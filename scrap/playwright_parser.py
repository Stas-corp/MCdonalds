from playwright.async_api import async_playwright

class BrowserClient:
    def __init__(self):
        self.playwright = None
        self.browser = None


    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.webkit.launch(headless=True)


    async def get_page_html(
        self, 
        url: str, 
        click_selector: str = None, 
        wait_selector: str = None
    ) -> str:
        context = await self.browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url)
            if click_selector:
                await page.click(click_selector)
            if wait_selector:
                await page.wait_for_selector(wait_selector)
            return await page.content()
        except Exception as e:
            raise ValueError(f"Playwright error: \n {e}")
        finally:
            await context.close()


    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()