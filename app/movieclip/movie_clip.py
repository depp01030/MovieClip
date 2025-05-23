import os
import aiohttp
import asyncio
from playwright.async_api import async_playwright
#from app.movieclip.config import ENTRANCEPOINT_URL

SEARCH_TERM = "i am surprised"
SEARCH_URL = "https://clip.cafe/?s={0}&usersearch=1&ss=s"
# SEARCH_URL = "https://yarn.co/yarn-find?text=i%20am%20surprised"
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
    user_data_dir = "/tmp/playwright-chrome-profile"
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            args=[],
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(search_url)
        # 模擬真人滑鼠移動
        await page.mouse.move(100, 100)
        await page.wait_for_timeout(500)
        await page.mouse.move(200, 200)
        await page.wait_for_timeout(500)
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
 

 
        await context.close()
        print("🏁 所有任務完成")

