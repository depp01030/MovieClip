import os
from app.movieclip.movie_clip import scrape_videos
from app.movieclip.add_srt import create_srt_for_folder
from app.movieclip.combine_mp4nsrt import combine_srt_for_folder
from app.movieclip.combine_videos import merge_videos
#%%
def file_reset(term_folder: str):
    """
    清除資料夾中的所有 mp4 和 srt 檔案
    :param term_folder: 資料夾路徑
    """
    for filename in os.listdir(term_folder):
        if (filename.endswith("sub.mp4") or 
            filename.startswith("merge") or 
            filename.endswith("list.txt") or 
            filename.endswith(".ass") or 
            filename.endswith(".srt")) :
            file_path = os.path.join(term_folder, filename)
            os.remove(file_path)
            print(f"❌ 刪除檔案：{file_path}")
            
async def run():
    search_term = "are you serious"
    # await scrape_videos(search_term = search_term)
    term_folder = os.path.join("downloads", search_term)
    file_reset(term_folder=term_folder)
    input('請確認資料夾已清空，按 Enter 繼續...')
    ## 這邊是將 mp4 轉成 srt
    create_srt_for_folder(term_folder = term_folder)
    ## 這邊是將 mp4 和 srt 合併
    combine_srt_for_folder(term_folder=term_folder)

    ## 這邊是將字幕檔案合併
    merge_videos(term_folder=term_folder)