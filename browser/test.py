from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://www.google.com/maps", wait_until="domcontentloaded")

    page.wait_for_timeout(10000)

    print("=" * 40)
    print("TITLE:", page.title())
    print("URL:", page.url)
    print("=" * 40)

    print(page.content())

    input("Press Enter...")