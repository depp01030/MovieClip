import os
from app.movieclip.movie_clip import scrape_videos
from app.movieclip.add_srt import create_srt_for_folder
from app.movieclip.combine_mp4nsrt import combine_srt_for_folder
from app.movieclip.combine_videos import merge_videos
from app.movieclip.video_decorate import generate_vertical_video
#%%
def file_reset(term_folder: str):
    """
    清除資料夾中的所有 mp4 和 srt 檔案
    :param term_folder: 資料夾路徑
    """
    for filename in os.listdir(term_folder):
        if (filename.endswith("sub.mp4") or 
            filename.endswith("shorts.mp4") or 
            filename.startswith("merge") or 
            filename.endswith("list.txt") or 
            filename.endswith(".ass") or 
            filename.endswith(".srt")) :
            file_path = os.path.join(term_folder, filename)
            os.remove(file_path)
            print(f"❌ 刪除檔案：{file_path}")

async def run():
    search_term = "its not about"
    english_line = "It's not about..."
    chinese_line = "這跟...無關。"
    
    search_term = "didnt see that comming"
    english_line = "I didn't see that coming"
    chinese_line = "我完全沒料到。"

    # await scrape_videos(search_term = search_term)
    term_folder = os.path.join("downloads", search_term)
    file_reset(term_folder=term_folder)
    input('請確認資料夾已清空，按 Enter 繼續...')
    ## 這邊是將 mp4 轉成 srt
    create_srt_for_folder(term_folder = term_folder)
    # 這邊是將 mp4 和 srt 合併
    combine_srt_for_folder(term_folder=term_folder)

    ## 這邊是將字幕檔案合併
    merge_videos(term_folder=term_folder)

    ## 這邊是將影片轉成直式影片
    generate_vertical_video(term_folder=term_folder,
                            english_line=english_line,
                            chinese_line=chinese_line)
    print("✅ 影片處理完成！")