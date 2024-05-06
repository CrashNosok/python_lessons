import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            proxy={
                'server': '',
                'username': '',
                'password': ''
            }
        )

        context = await browser.new_context()

        page = await context.new_page()

        await page.goto('https://2ip.ru')

        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
