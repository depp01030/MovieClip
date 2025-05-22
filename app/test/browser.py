# app/browser.py
from playwright.async_api import async_playwright
from app.test.config import ENTRANCEPOINT_URL
async def launch_browser(headless=True):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    page = await browser.new_page()
    await page.goto(ENTRANCEPOINT_URL)  # 可以先改成你要測試的網址
    return browser, page
