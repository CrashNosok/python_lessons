import asyncio

from playwright.async_api import async_playwright, expect


EXTENTION_PATH = ''
MM_PASSWORD = ''


async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENTION_PATH}",
                f"--load-extension={EXTENTION_PATH}",
            ],
            # slow_mo=600
        )

        if len(context.background_pages) == 0:
            background_page = await context.wait_for_event('backgroundpage')
        else:
            background_page = context.background_pages[0]

        titles = [await p.title() for p in context.pages]
        while 'MetaMask' not in titles:
            titles = [await p.title() for p in context.pages]

        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()

        # -------------------- согласиться с условиями использования и создать новый кошелек --------------------
        checkbox = mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-create-wallet')
        await expect(create_wallet_btn).to_be_enabled()
        await create_wallet_btn.click()

        # -------------------- отказаться от сбора информации --------------------
        i_dont_agree_btn = mm_page.get_by_test_id(test_id='metametrics-no-thanks')
        await expect(i_dont_agree_btn).to_be_attached()
        await i_dont_agree_btn.click()

        # -------------------- ввести пароль --------------------
        passwd_1 = mm_page.get_by_test_id(test_id='create-password-new')
        passwd_2 = mm_page.get_by_test_id(test_id='create-password-confirm')
        checkbox = mm_page.get_by_test_id(test_id='create-password-terms')
        create_wallet_btn = mm_page.get_by_test_id(test_id='create-password-wallet')
        await expect(passwd_1).to_be_attached()
        await passwd_1.fill(MM_PASSWORD)
        await passwd_2.fill(MM_PASSWORD)
        await checkbox.click()

        await expect(create_wallet_btn).to_be_enabled()
        await create_wallet_btn.click()

        # -------------------- защитить кошелек --------------------
        protect_wallet_btn = mm_page.get_by_test_id(test_id='secure-wallet-recommended')
        await expect(protect_wallet_btn).to_be_attached()
        await protect_wallet_btn.click()

        # -------------------- показать секретную фразу --------------------
        show_seed_btn = mm_page.get_by_test_id(test_id='recovery-phrase-reveal')
        await expect(show_seed_btn).to_be_attached()
        await show_seed_btn.click()

        seed = []
        for i in range(12):
            seed.append(
                await mm_page.get_by_test_id(test_id=f'recovery-phrase-chip-{i}').inner_text()
            )
        print(seed)

        continue_btn = mm_page.get_by_test_id(test_id='recovery-phrase-next')
        await continue_btn.click()

        # -------------------- подтвердить секретную фразу --------------------
        seed_field = mm_page.get_by_test_id(test_id='recovery-phrase-input-2')
        await expect(seed_field).to_be_attached()

        await mm_page.get_by_test_id(test_id='recovery-phrase-input-2').fill(seed[2])
        await mm_page.get_by_test_id(test_id='recovery-phrase-input-3').fill(seed[3])
        await mm_page.get_by_test_id(test_id='recovery-phrase-input-7').fill(seed[7])

        confirm_btn = mm_page.get_by_test_id(test_id='recovery-phrase-confirm')
        await expect(confirm_btn).to_be_enabled()
        await confirm_btn.click()

        # -------------------- нажать "понятно" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-complete-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- нажать "далее" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-next')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- нажать "выполнено" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- закрыть страничку --------------------
        await mm_page.close()

        await asyncio.sleep(100)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())
