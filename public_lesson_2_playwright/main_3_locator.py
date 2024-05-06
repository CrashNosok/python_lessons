import asyncio

from playwright.async_api import async_playwright, expect


async def main():
    uniswap_url = 'https://app.uniswap.org/swap'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # инициалиировать контекст
        # https://playwright.dev/python/docs/api/class-browsercontext
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(uniswap_url)

        # await page.wait_for_load_state(state='domcontentloaded')
        '''
        использование state='networkidle' не рекомендуется 
        https://playwright.dev/python/docs/api/class-frame#frame-wait-for-load-state
        в документации сказано: 
        "Don't use this method for testing, rely on web assertions to assess readiness instead."

        И мы могли бы использовать дополнительную задержку
        await page.wait_for_timeout(2000)  # Задержка в 2 секунды
        '''

        # поиск по placeholder
        # inputs = page.get_by_placeholder('0')

        # поиск по css selector
        inputs = page.locator('input')

        # такой способ не успеет найти элемент так как сработает до полной загрузки страницы
        # !! устаревший метод !!
        # !! возвращает ElementHandle, а не Locator !!
        # input_ = await page.query_selector('input')

        '''
        вместо wait_for_load_state(state='networkidle') можно использовать assertions
        но применять нужно к конкретному элементу, а не ко всем сразу
        '''
        await expect(inputs.first).to_be_visible()

        await asyncio.sleep(1000)

        print(len(await inputs.all()))

        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
