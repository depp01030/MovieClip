# app/form_filler.py

async def fill_form(page):
    print("🔤 填寫表單中...")

    # 這邊以 httpbin.org 的 form 為例

    await page.get_by_role("textbox", name="電話號碼/使用者名稱/Email").click()
    await page.get_by_role("textbox", name="電話號碼/使用者名稱/Email").fill("0981595136")
    await page.get_by_role("textbox", name="密碼").click()
    await page.get_by_role("textbox", name="密碼").fill("evensa0301")
    await page.get_by_role("button", name="登入").click()
    await page.get_by_role("button", name="使用簡訊驗證").click()
    await page.get_by_role("button", name="登入").click()
 