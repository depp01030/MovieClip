import os
from app.movieclip.movie_clip import scrape_videos
from app.movieclip.add_srt import create_srt_for_folder
from app.movieclip.combine_mp4nsrt import combine_srt_for_folder
from app.movieclip.combine_videos import merge_videos
#%%
async def run():
    search_term = "i am ok with that"
    await scrape_videos(search_term = search_term)
    term_folder = os.path.join("downloads", search_term)

    ## 這邊是將 mp4 轉成 srt
    create_srt_for_folder(term_folder = term_folder)
    ## 這邊是將 mp4 和 srt 合併
    combine_srt_for_folder(term_folder=term_folder)

    ## 這邊是將字幕檔案合併
    merge_videos(term_folder=term_folder)