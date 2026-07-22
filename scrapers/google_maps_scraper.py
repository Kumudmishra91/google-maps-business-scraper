from playwright.sync_api import Page, TimeoutError
import csv


class GoogleMapScraper:
    """
    Handles searching and scraping businesses from Google Maps.
    """

    def __init__(self, page: Page, query: str):
        self.page = page
        self.query = query

        # Stores all unique business links
        self.business_links = []

        # Stores scraped business details
        self.business_data = []
    # STEP 1 : Open Google Maps
    def open_google_maps(self):

        print("\n" + "=" * 80)
        print("STEP 1 : OPEN GOOGLE MAPS")
        print("=" * 80)

        self.page.goto(
            "https://www.google.com/maps",
            wait_until="domcontentloaded",
            timeout=60000
        )

        self.page.wait_for_timeout(5000)

        print("\n========== DEBUG ==========")
        print("Search box count :", self.page.locator("#searchboxinput").count())
        print("Input count      :", self.page.locator("input").count())
        print("Button count     :", self.page.locator("button").count())
        print("===========================\n")

        print(f"Current URL  : {self.page.url}")
        print(f"Page Title   : {self.page.title()}")

        print("Google Maps opened successfully.\n")
    # STEP 2 : Search Business
    def search_business(self):

        print("\n" + "=" * 80)
        print("STEP 2 : SEARCH BUSINESS")
        print("=" * 80)

        print(f"Searching for: {self.query}")

        selectors = [
            "#searchboxinput",
            "input[placeholder='Search Google Maps']",
            "input[aria-label='Search Google Maps']",
            "input[type='text']",
            "input"
        ]

        for selector in selectors:

            try:

                locator = self.page.locator(selector)

                # Wait for the element to appear
                try:
                    locator.first.wait_for(timeout=10000)
                except:
                    print(f"{selector} not found.")
                    continue

                print(f"Trying selector -> {selector}")

                # Print the HTML of the element we're interacting with
                print(locator.first.evaluate("el => el.outerHTML"))

                # Click the search box
                locator.first.click()

                # Clear existing text
                locator.first.fill("")

                # Type the query like a real user
                locator.first.type(self.query, delay=80)

                # Press Enter
                locator.first.press("Enter")

                # Wait for navigation/results
                self.page.wait_for_load_state("domcontentloaded")
                self.page.wait_for_timeout(5000)

                print("=" * 50)
                print("AFTER SEARCH")
                print("=" * 50)
                print("URL:", self.page.url)
                print("TITLE:", self.page.title())
                print("Current URL:", self.page.url)
                print("Page Title:", self.page.title())
                print("Search submitted successfully.")

                return

            except Exception as e:
                print(f"{selector} failed : {e}")

        raise Exception("Could not locate Google Maps search box.")
    # STEP 3 : Wait For Search Results
    def wait_for_results(self):

        print("\n" + "=" * 80)
        print("STEP 3 : WAIT FOR RESULTS")
        print("=" * 80)

        possible_selectors = [
            'div[role="feed"]',
            '[role="feed"]',
            'div[aria-label*="Results"]',
            '.m6QErb'
        ]

        for selector in possible_selectors:

            try:

                print(f"Checking selector : {selector}")

                self.page.wait_for_selector(
                    selector,
                    timeout=30000
                )

                print(f"Results panel found using: {selector}")

                return selector

            except TimeoutError:

                print(f"Not found : {selector}")
                """self.page.screenshot(
    path="debug.png",
    full_page=False,
    animations="disabled",
    timeout=5000
)"""

                print(self.page.content()[:3000])
        raise Exception("Search results panel could not be located.")
    # STEP 4 : Scroll Results (To be implemented next)
    def scroll_results(self, panel_selector):

        print("\n" + "=" * 80)
        print("STEP 4 : SCROLL RESULTS")
        print("=" * 80)

        scroll_panel = self.page.locator(panel_selector).first

        previous_height = 0
        same_height_count = 0
        scroll_count = 0

        while True:

            current_height = scroll_panel.evaluate(
                "(element) => element.scrollHeight"
            )

            print(f"\nScroll #{scroll_count + 1}")
            print(f"Current Height : {current_height}")

            scroll_panel.evaluate(
                "(element) => element.scrollTo(0, element.scrollHeight)"
            )

            self.page.wait_for_timeout(2000)

            new_height = scroll_panel.evaluate(
                "(element) => element.scrollHeight"
            )

            print(f"New Height : {new_height}")

            if new_height == previous_height:

                same_height_count += 1

                print(
                    f"No new content loaded "
                    f"({same_height_count}/3)"
                )

            else:

                same_height_count = 0

            previous_height = new_height
            scroll_count += 1

            if same_height_count >= 3:

                print("\nReached end of available results.")
                break

                print(f"\nTotal Scrolls Performed : {scroll_count}")
    # STEP 5 : Collect Business Cards (To be implemented later)

    def collect_business_cards(self):

        print("\n" + "=" * 80)
        print("STEP 5 : COLLECT BUSINESS CARDS")
        print("=" * 80)

        print("Business card collection will be implemented later.")
    # MAIN SCRAPE PIPELINE
    def scrape_business_details(self):

        print("\n" + "=" * 80)
        print("SCRAPING BUSINESS DETAILS")
        print("=" * 80)

        business = {}

        # Current URL
        business["url"] = self.page.url

        # Name
        try:
            business["name"] = self.page.locator("h1").first.inner_text().strip()
        except:
            business["name"] = ""

        # Rating
        try:
            business["rating"] = self.page.locator('span[role="img"]').first.get_attribute("aria-label")
        except:
            business["rating"] = ""

        print(business)

        return business
    def scrape(self):

        self.open_google_maps()

        self.search_business()

        panel_selector = self.wait_for_results()

        self.scroll_results(panel_selector)

        self.collect_business_links()

        print("\nStarting business scraping...\n")

        for index, link in enumerate(self.business_links, start=1):

            print("=" * 80)
            print(f"Business {index}/{len(self.business_links)}")
            print(link)

            try:
                self.page.goto(
                    link,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                self.page.wait_for_timeout(3000)

                print(f"Opened: {self.page.title()}")

                print("Calling scrape_business_details()...")

                business = self.scrape_business_details()

                print("Returned:", business)
                if business:
                    self.business_data.append(business)         
            except Exception as e:
                print(f"Failed to scrape business: {e}")
        self.save_to_csv()       
                
    def collect_business_links(self):

        print("\n" + "=" * 80)
        print("STEP 5 : COLLECT BUSINESS LINKS")
        print("=" * 80)

        cards = self.page.locator('a[href*="/place/"]')

        total_cards = cards.count()

        print(f"Business cards found : {total_cards}")

        for i in range(total_cards):

            try:

                href = cards.nth(i).get_attribute("href")

                if href and href not in self.business_links:

                    self.business_links.append(href)

                    print(f"[{len(self.business_links)}] {href}")

            except Exception as e:

                print(f"Error reading card {i + 1}: {e}")

        print("\n" + "=" * 80)
        print(f"Collected {len(self.business_links)} Unique Business Links")
        print("=" * 80)
    def scrape_business_details(self):
        """
        Scrapes details of the currently opened Google Maps business page.
        Returns a dictionary containing the extracted information.
        """

        print("\n" + "=" * 80)
        print("SCRAPING BUSINESS DETAILS")
        print("=" * 80)

        self.page.wait_for_timeout(3000)

        # -------------------------
        # Name
        # -------------------------
        name = "N/A"

        name_selectors = [
            "h1.DUwDvf",
            "h1.fontHeadlineLarge",
            "h1"
        ]

        for selector in name_selectors:
            try:
                locator = self.page.locator(selector).first

                if locator.count() > 0:
                    text = locator.inner_text().strip()

                    if text:
                        name = text
                        break
            except:
                pass

        # -------------------------
        # Category
        # -------------------------
        category = "N/A"

        try:
            locator = self.page.locator(
                'button[jsaction*="pane.rating.category"]'
            ).first

            if locator.count() > 0:
                category = locator.inner_text().strip()

        except:
            pass

        # -------------------------
        # Rating
        # -------------------------
        rating = "N/A"

        rating_selectors = [
            'div[role="main"] span[aria-hidden="true"]',
            'span[role="img"]',
            'div.F7nice span'
        ]

        for selector in rating_selectors:
            try:
                locator = self.page.locator(selector).first

                if locator.count() > 0:
                    text = locator.inner_text().strip()

                    if text:
                        rating = text
                        break
            except:
                pass

        # -------------------------
        # Reviews
        # -------------------------
        reviews = "N/A"

        try:
            locator = self.page.locator(
                'button[jsaction*="pane.rating.moreReviews"]'
            ).first

            if locator.count() > 0:
                reviews = locator.inner_text().strip()

        except:
            pass

        # -------------------------
        # Address
        # -------------------------
        address = "N/A"

        try:
            locator = self.page.locator(
                'button[data-item-id="address"]'
            ).first

            if locator.count() > 0:
                address = locator.inner_text().strip()

        except:
            pass

        # -------------------------
        # Phone
        # -------------------------
        phone = "N/A"

        try:
            locator = self.page.locator(
                'button[data-item-id^="phone"]'
            ).first

            if locator.count() > 0:
                phone = locator.inner_text().strip()

        except:
            pass

        # -------------------------
        # Website
        # -------------------------
        website = "N/A"

        try:
            locator = self.page.locator(
                'a[data-item-id="authority"]'
            ).first

            if locator.count() > 0:
                href = locator.get_attribute("href")

                if href:
                    website = href

        except:
            pass

        # -------------------------
        # Opening Hours
        # -------------------------
        hours = "N/A"

        try:
            locator = self.page.locator(
                'button[data-item-id="oh"]'
            ).first

            if locator.count() > 0:
                hours = locator.inner_text().strip()

        except:
            pass

        # -------------------------
        # Latitude & Longitude
        # -------------------------
        latitude = "N/A"
        longitude = "N/A"

        try:
            url = self.page.url

            if "@" in url:
                coords = url.split("@")[1].split(",")

                latitude = coords[0]
                longitude = coords[1]

        except:
            pass

        business = {
            "name": name,
            "category": category,
            "rating": rating,
            "reviews": reviews,
            "address": address,
            "phone": phone,
            "website": website,
            "hours": hours,
            "latitude": latitude,
            "longitude": longitude,
            "link": self.page.url
        }

        print(f"Name      : {name}")
        print(f"Category  : {category}")
        print(f"Rating    : {rating}")
        print(f"Reviews   : {reviews}")
        print(f"Address   : {address}")
        print(f"Phone     : {phone}")
        print(f"Website   : {website}")
        print(f"Hours     : {hours}")
        print(f"Latitude  : {latitude}")
        print(f"Longitude : {longitude}")

        return business
    def save_to_csv(self):

        if not self.business_data:
            print("No business data to save.")
            return

        filename = "output/google_maps_data.csv"

        headers = self.business_data[0].keys()

        with open(filename, "w", newline="", encoding="utf-8-sig") as file:

            writer = csv.DictWriter(file, fieldnames=headers)

            writer.writeheader()

            writer.writerows(self.business_data)

        print("\n" + "=" * 80)
        print("CSV SAVED SUCCESSFULLY")
        print("=" * 80)
        print(f"Location : {filename}")
        print(f"Businesses Saved : {len(self.business_data)}")