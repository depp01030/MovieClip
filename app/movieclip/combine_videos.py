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
        for filename in sorted(os.listdir(term_folder)):
            # 只合併 _sub.mp4，避免原始 mp4 編碼不一致
            if filename.endswith("_sub.mp4"):
                video_path = os.path.join(os.getcwd(), term_folder, filename)
                f.write(f"file '{Path(video_path)}'\n")
    # ffmpeg 合併命令（重新編碼，強制音訊參數）
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264",    # 重新編碼影片
        "-preset", "fast",    # 編碼速度
        "-crf", "23",         # 視覺品質
        "-c:a", "aac",        # 音訊編碼
        "-b:a", "128k",       # 音訊比特率
        "-ar", "44100",       # 音訊取樣率
        "-ac", "2",           # 聲道數
        "-movflags", "+faststart",  # for streaming compatibility
        "-fflags", "+genpts",       # 產生正確時間軸
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ 合併完成：{output_path}")

# 使用範例
if __name__ == "__main__":
    term_folder = "downloads/i am surprised"
    merge_videos(term_folder=term_folder)
