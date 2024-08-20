import json
import os
import re

import requests
from bs4 import BeautifulSoup

json_filename = "torrents.json"
if os.path.exists(json_filename):
    with open(json_filename, "r", encoding="utf-8") as json_file:
        missing_torrents_info = json.load(json_file)
else:
    missing_torrents_info = {}

for page in range(1, 6):
    url = f"https://nyaa.si/?page={page}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    torrent_entries = soup.find_all("tr", class_=re.compile("default|success|danger"))

    ids = []
    for entry in torrent_entries:
        tds = entry.find_all("td")
        a_tag = tds[1].find("a")["href"]
        id = a_tag.replace("/view/", "")
        if "#" in id:
            id = id.split("#")[0]
        ids.append(int(id))

    ids.sort()
    missing_ids = [i for i in range(ids[0], ids[-1] + 1) if i not in ids]

    def get_torrent_info(torrent_id):
        urls = [
            ("https://nyaa.si/view/", "hidden"),
            ("https://nyaa.land/view/", "deleted"),
        ]
        for base_url, status in urls:
            torrent_url = f"{base_url}{torrent_id}"
            response = requests.get(torrent_url)
            if response.status_code == 200:
                if (
                    "404 Not Found" in response.text
                    or "The path you requested does not exist on this server"
                    in response.text
                ):
                    continue
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.find("h3", class_="panel-title").text.strip()

                size_label_div = soup.find("div", string=re.compile(r"File size:"))
                size = (
                    size_label_div.find_next("div").text.strip()
                    if size_label_div
                    else None
                )

                magnet_link = soup.find("a", href=re.compile(r"magnet:\?xt=urn:btih:"))
                info_hash = (
                    re.search(r"btih:([a-zA-Z0-9]+)", magnet_link["href"]).group(1)
                    if magnet_link
                    else None
                )

                date_div = soup.find("div", string=re.compile(r"Date:"))
                timestamp = (
                    int(date_div.find_next("div")["data-timestamp"])
                    if date_div and "data-timestamp" in date_div.find_next("div").attrs
                    else None
                )

                submitter_div = soup.find("div", string=re.compile(r"Submitter:"))
                submitter = (
                    submitter_div.find_next("div").text.strip()
                    if submitter_div
                    else None
                )

                category_links = soup.find_all("a", href=re.compile(r"/\?c="))
                if len(category_links) >= 2:
                    category = category_links[1]["href"].replace("/?c=", "")
                else:
                    category = None

                return {
                    "title": title,
                    "size": size,
                    "info_hash": info_hash,
                    "status": status,
                    "timestamp": timestamp,
                    "submitter": submitter,
                    "category": category
                }
        return None

    for missing_id in missing_ids:
        info = get_torrent_info(missing_id)
        if info:
            existing_info = missing_torrents_info.get(str(missing_id))
            if not existing_info or (
                existing_info.get("title") != info["title"]
                or existing_info.get("size") != info["size"]
                or existing_info.get("info_hash") != info["info_hash"]
                or existing_info.get("timestamp") != info["timestamp"]
                or existing_info.get("submitter") != info["submitter"]
                or existing_info.get("category") != info["category"]
            ):
                missing_torrents_info[str(missing_id)] = info

    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(
            missing_torrents_info, json_file, ensure_ascii=False, separators=(",", ":")
        )
