import subprocess
from pathlib import Path
import os
#%%
def burn_subtitle(video_path: str, subtitle_path: str, output_path: str):
    # 確保路徑都存在
    video = Path(video_path)
    subtitle = Path(subtitle_path)

    if not video.exists():
        raise FileNotFoundError(f"影片不存在：{video}")
    if not subtitle.exists():
        raise FileNotFoundError(f"字幕不存在：{subtitle}")

    # 建立輸出資料夾（如果需要）
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # ffmpeg 命令
    cmd = [
        "ffmpeg",
        "-i", str(video),
        "-vf", f"subtitles={subtitle}",  # 注意：subtitles 這邊 ffmpeg 不接受引號，要當字串
        "-c:a", "copy",                  # 保留原始音訊
        str(output_path)
    ]

    # 執行命令
    subprocess.run(cmd, check=True)
    print(f"✅ 已輸出：{output_path}")
def combine_srt_for_folder(term_folder):
    """
    將資料夾中的所有 mp4 和 srt 檔案合併
    :param term_folder: 資料夾路徑
    """
    for filename in os.listdir(term_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(term_folder, filename)
            print(f"🔍 合併字幕檔案：{video_path}")
            srt_path = video_path.replace(".mp4", ".srt")  # 假設視頻是 mp4 格式

            if os.path.exists(srt_path):
                output_path = video_path.replace(".mp4", "_sub.mp4")
                burn_subtitle(video_path, srt_path, output_path)
            else:
                print(f"❌ 找不到字幕檔：{srt_path}")

if __name__ == "__main__":

    video_path="downloads/i am surprised/1.mp4"
    subtitle_path="downloads/i am surprised/1.srt"
    output_path="downloads/i am surprised/subtitle.mp4"
    # burn_subtitle(
    #     video_path=video_path,
    #     subtitle_path=subtitle_path,
    #     output_path=output_path
    # )
    term_folder = "downloads/i am surprised"
    combine_srt_for_folder(term_folder=term_folder)