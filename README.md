# Torrent Info Scraper

## Description

The `main.py` Python script is designed to update information about missing torrents from Nyaa.si and Nyaa.land. It extracts data about missing torrents by checking the torrent pages on these sites and updates a JSON file (`torrents.json`) with the extracted information.

## Features

- **Automated Torrent Retrieval**: Identifies missing torrents by checking pages on Nyaa.si and Nyaa.land.
- **Data Extraction**: Extracts the following information for each missing torrent:
  - Torrent title
  - File size
  - Info hash
  - Publication date (timestamp)
  - Submitter of the torrent
  - Status of the torrent (whether available or deleted)
- **JSON File Update**: Updates `torrents.json` with the latest information. Existing entries are updated if any details have changed.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `lxml` (required for BeautifulSoup)

You can install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

## JSON File Structure

The `torrents.json` file contains a dictionary where each key is the ID of a missing torrent, and each value is a dictionary with the following information:

- `title`: Torrent title
- `size`: File size
- `info_hash`: Torrent info hash
- `status`: Torrent status (`hidden` or `deleted`)
- `timestamp`: Publication date of the torrent (in Unix timestamp)
- `submitter`: Submitter of the torrent

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Notes

- The script uses regular expressions to extract specific information from web pages.
- Ensure compliance with the rules and terms of service of the websites accessed by this script.
