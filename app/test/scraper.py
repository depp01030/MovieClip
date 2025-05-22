# app/scraper.py

async def scrape_data(page):
    print("🔍 擷取資料中...")
    content = await page.text_content("body")
    print("✅ 擷取成功！")
    print(content[:300])  # 顯示前 300 字


# scrape_minuet.py
import asyncio
from playwright.async_api import async_playwright
from playwright.async_api import async_playwright
import asyncio
from playwright.async_api import async_playwright
import asyncio

async def scrape():
    url = "https://en.love-minuet.com/product/koon-stripe-pants-3color/17339/category/1/display/3/"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)
        await page.wait_for_selector("#prdDetail")

        title = await page.locator("div.headingArea h2").inner_text()
        desc = await page.locator("#prdDetail").inner_text()
        # desc_html = await page.locator("#prdDetail").inner_html()

        print("🛍️ 商品名稱：", title)
        print("📄 商品說明文字：\n", desc[:300], "...")

        await browser.close()
 