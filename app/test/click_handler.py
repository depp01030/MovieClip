# app/click_handler.py

async def click_buttons(page):
    print("🖱️ 點選按鈕中...")
    await page.click('text=Submit order')  # 提交按鈕
    await page.wait_for_timeout(2000)  # 等 2 秒看效果
