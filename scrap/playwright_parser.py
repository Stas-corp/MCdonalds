from playwright.sync_api import sync_playwright

class BrowserClient:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch(headless=True)

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
        except:
            raise ValueError("Playwright error")
        finally:
            page.close()

    def close(self):
        self.browser.close()
        self.playwright.stop()