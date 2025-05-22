import os
import aiohttp
import asyncio
from playwright.async_api import async_playwright
#from app.movieclip.config import ENTRANCEPOINT_URL

SEARCH_TERM = "i am surprised"
SEARCH_URL = "https://clip.cafe/?s={0}&usersearch=1&ss=s"
#SEARCH_URL = "https://yarn.co/yarn-find?text=i%20am%20surprised"
import os

async def download_video(url, save_path):
    # 🧱 確保資料夾存在
    folder = os.path.dirname(save_path)
    os.makedirs(folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(save_path, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024*1024)
                    if not chunk:
                        break
                    f.write(chunk)

    print(f"✅ 下載完成：{save_path}")

 

async def scrape_videos(search_term):
    print("🎬 [movieclip] 任務開始")
    search_url = SEARCH_URL.format(search_term.replace(" ","+")) 
    print(f"🔍 搜尋網址：{search_url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(search_url)

        # await page.fill('#search-input', serching_term)
 
        # await page.click('#searchbox-frontpage > button')
        
        await page.wait_for_selector("#main-cont > div.searchResults > div")

        # 取得所有搜尋結果卡片
        cards = await page.locator("#main-cont > div.searchResults > div").all()
        print(f"🔍 找到 {len(cards)} 個影片卡片")

        # 用來存抓到的 mp4 連結，避免重複下載
        found_videos = set()

        # 監聽所有請求
        async def on_request(request):
            url = request.url
            if 'blank' not in url and url.endswith(".mp4") and url not in found_videos:
                found_videos.add(url)
                print(f"🎯 偵測到影片請求：{url}")
                # 自動下載
                index = len(found_videos)
                save_path = f"downloads/{search_term}/{index}.mp4"
                await download_video(url, save_path)

        page.on("request", on_request)

        # hover 所有預覽圖來觸發影片請求
        for i, card in enumerate(cards[:3]):
            print(f"\n🖱️ Hover 第 {i+1} 張卡片")
            hover_target = card.locator("div.searchResultClipImg")
            await hover_target.hover()
            await page.wait_for_timeout(3000)  # 等 3 秒
 

 
        await browser.close()
        print("🏁 所有任務完成")

 