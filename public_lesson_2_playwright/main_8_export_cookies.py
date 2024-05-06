import json
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )

        context = await browser.new_context()

        page = await context.new_page()

        await page.goto('https://coinmarketcap.com/')

        # получить куки
        cookies = await context.cookies()
        print(cookies)

        theme_button = page.locator(
            '//*[@id="__next"]/div[2]/div[1]/div[1]/div[2]/div[1]/section/div/div[1]/div/div[2]/div[1]/button')
        await expect(theme_button).to_be_visible()
        await theme_button.click()

        cookies = await context.cookies()
        print(cookies)

        Path("cookies.json").write_text(json.dumps(cookies))

        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
