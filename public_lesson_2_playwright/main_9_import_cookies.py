import json
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )

        context = await browser.new_context()

        # добавить куки
        await context.add_cookies(json.loads(Path("cookies.json").read_text()))

        page = await context.new_page()

        await page.goto('https://coinmarketcap.com/')
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
