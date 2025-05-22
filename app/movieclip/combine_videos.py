import subprocess
from pathlib import Path
import os

#%%
def merge_videos(term_folder):
    output_path = os.path.join(term_folder, "merged_video.mp4")
    # 產生清單檔案
    merger_list_path = os.path.join(term_folder, "merge_list.txt")
    list_file = Path(merger_list_path)
    with open(list_file, "w", encoding="utf-8") as f: 
        for filename in os.listdir(term_folder):
            if filename.endswith("sub.mp4") :

                video_path = os.path.join(os.getcwd(),term_folder, filename)
                 
                f.write(f"file '{Path(video_path)}'\n")

    # ffmpeg 合併命令
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ 合併完成：{output_path}")

# 使用範例
if __name__ == "__main__":
    term_folder = "downloads/i am surprised"
    
    merge_videos(term_folder=term_folder)
