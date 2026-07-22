# Google Maps Business Scraper

## Project Overview

This project is a Google Maps Business Scraper built using Python and Playwright. It automates the process of searching businesses on Google Maps, collecting business links, extracting business information, and exporting the results into a CSV file.

---

## Features

- Search businesses by keyword
- Automatically scroll through Google Maps results
- Collect business profile links
- Extract:
  - Business Name
  - Category
  - Rating
  - Reviews
  - Address
  - Phone Number
  - Website
  - Opening Hours
  - Latitude
  - Longitude
  - Google Maps URL
- Export data to CSV

---

## Technologies Used

- Python
- Playwright
- CSV Module
- Google Maps

---

## Project Structure

```
project_scraper/
│
├── browser/
├── scrapers/
├── output/
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## How to Run

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Install Playwright

```bash
playwright install
```

3. Run the scraper

```bash
python main.py
```

---

## Output

The scraper generates:

```
output/google_maps_data.csv
```

---

## Author

Kumud Mishra