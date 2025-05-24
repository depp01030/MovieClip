import subprocess
from pathlib import Path
import os
#%%
def burn_subtitle(video_path: str, subtitle_path: str, output_path: str):
    # 確保路徑都存在
    mp4_file = Path(video_path).resolve()
    subtitle = Path(subtitle_path).resolve()
    output_file = Path(output_path).resolve()

    if not mp4_file.exists():
        raise FileNotFoundError(f"影片不存在：{mp4_file}")
    if not subtitle.exists():
        raise FileNotFoundError(f"字幕不存在：{subtitle}")

    # 建立輸出資料夾（如果需要）
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # ffmpeg filter 參數要 escape 特殊字元
    # 先調整成 16:9 再加字幕，避免字幕被裁切
    scale_crop_filter = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
    subtitle_filter = "ass='{}'".format(str(subtitle).replace("'", r"\\'"))
    vf_filter = f"{scale_crop_filter},{subtitle_filter}"

    cmd = [
        "ffmpeg",
        "-i", str(mp4_file),
        "-vf", vf_filter,
        "-map", "0:v:0",
        "-map", "0:a:0?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-ac", "2",
        "-movflags", "+faststart",
        str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ ffmpeg 轉換失敗：{mp4_file.name}")
        print(e)

def combine_srt_for_folder(term_folder):
    """
    將資料夾中的所有 mp4 和 srt 檔案合併
    :param term_folder: 資料夾路徑
    """
    for filename in os.listdir(term_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(term_folder, filename)
            print(f"🔍 合併字幕檔案：{video_path}")
            srt_path = video_path.replace(".mp4", ".ass")  # 假設視頻是 mp4 格式

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