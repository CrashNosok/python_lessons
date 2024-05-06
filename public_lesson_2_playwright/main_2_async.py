import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
        await page.screenshot(path='./demo.png')
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
