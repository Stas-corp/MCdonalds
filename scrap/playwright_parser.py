from playwright.sync_api import sync_playwright

class BrowserClient:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def get_page_html(
        self, 
        url: str, 
        click_selector: str = None, 
        wait_selector: str = None
    ) -> str:
        page = self.browser.new_page()
        try:
            page.goto(url)
            if click_selector:
                page.click(click_selector)
            if wait_selector:
                page.wait_for_selector(wait_selector)
            return page.content()
        except Exception as e:
            raise ValueError(f"Playwright error: \n{e}")
        finally:
            page.close()

    def close(self) -> None:
        self.browser.close()
        self.playwright.stop()