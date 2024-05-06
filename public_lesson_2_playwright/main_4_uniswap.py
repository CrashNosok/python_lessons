import asyncio

from playwright.async_api import async_playwright, expect


DEFAULT_DELAY = 300
TO_TOKEN_ADDRESS = '0xdac17f958d2ee523a2206206994597c13d831ec7'  # USDT


async def main():
    uniswap_url = 'https://app.uniswap.org/swap'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(uniswap_url)

        inputs = page.get_by_placeholder('0')
        await expect(inputs.first).to_be_visible()

        await inputs.first.type('0.0001', delay=DEFAULT_DELAY)

        choose_token_button = page.locator('//*[@id="swap-currency-output"]/div/div[1]/div[2]/div/button')
        await expect(choose_token_button).to_be_visible()

        await choose_token_button.click()

        token_name_input = page.locator('#token-search-input')
        await expect(token_name_input).to_be_visible()
        await token_name_input.type(TO_TOKEN_ADDRESS)

        results = page.get_by_test_id('currency-list-wrapper')
        await expect(results).to_be_visible()

        # при копировании полного xpath, нужно начинать путь с "//", а не с "/"
        target_token = page.locator('//html/body/reach-portal[7]/div[2]/div/div/div/div/div[3]/div/div')

        # ждем, когда в нужном элементе появится нужный нам текст
        await expect(target_token).to_have_text(expected='Tether USDUSDT', timeout=5000)
        # эти способы не подойдут так как они проверяют на наличие элемента в DOM дереве
        # await expect(target_token).to_be_attached(timeout=5000)
        # await target_token.wait_for(timeout=5000, state='visible')
        # await target_token.wait_for(timeout=5000, state='attached')

        await target_token.click()

        await asyncio.sleep(10000)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
