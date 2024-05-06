import asyncio

from fake_useragent import FakeUserAgent

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Установка пользовательского агента
        # https://playwright.dev/python/docs/emulation#user-agent
        user_agent = FakeUserAgent().random
        print(user_agent)
        context = await browser.new_context(user_agent=user_agent)

        page = await context.new_page()

        await page.goto('https://whatmyuseragent.com/')

        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
