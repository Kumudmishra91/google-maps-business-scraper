from browser.browser_manager import BrowserManager
from scrapers.google_maps_scraper import GoogleMapScraper


def main():

    query = "restaurants in lucknow"

    browser = BrowserManager()

    page = browser.start_browser()

    scraper = GoogleMapScraper(page, query)
    try:
        scraper.scrape()

    except Exception as e:
        print("\nERROR:")
        print(e)
        input("\nPress Enter to close browser...")

    finally:
        browser.close_browser()
if __name__ == "__main__":
    main()