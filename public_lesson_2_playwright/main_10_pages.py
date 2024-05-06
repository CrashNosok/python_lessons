import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )

        context = await browser.new_context()

        page = await context.new_page()

        await page.goto('https://app.uniswap.org/swap')

        # открыть новую страницу
        page2 = await context.new_page()

        # получить список откртых страниц
        print(context.pages)

        await asyncio.sleep(3)

        # переключение на другую страницу
        await context.pages[0].bring_to_front()

        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
