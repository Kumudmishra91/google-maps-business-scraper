from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start_browser(self):

        print("Starting Playwright...")
        self.playwright = sync_playwright().start()

        print("Launching Chromium...")

        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=100,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-default-browser-check",
                "--disable-dev-shm-usage",
            ]
        )

        self.context = self.browser.new_context(
            viewport=None,                  # Use full screen
            ignore_https_errors=True,
            java_script_enabled=True,
            locale="en-US"
        )

        self.page = self.context.new_page()

        self.page.set_default_timeout(60000)

        print("Browser started successfully.\n")

        return self.page

    def close_browser(self):

        print("\nClosing Browser...")

        try:

            if self.page:
                self.page.close()

            if self.context:
                self.context.close()

            if self.browser:
                self.browser.close()

            if self.playwright:
                self.playwright.stop()

        except Exception as e:
            print(f"Error while closing browser: {e}")

        print("Browser Closed Successfully.")