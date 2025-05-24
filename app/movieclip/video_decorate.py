import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip

# ───────────── 變數區 ─────────────

# INPUT_PATH = "downloads/are you serious/merged_video.mp4"  # 輸入影片路徑
# OUTPUT_PATH = "downloads/are you serious/ig_shorts.mp4"  # 輸出影片路徑

# TOP_TEXT = "Are you serious?"  # 上方文字
BOTTOM_TEXT = "One quote a day"  # 下方文字

TOP_BAR_COLOR = (206, 198, 185)  # 上色塊：莫蘭迪灰粉
BOTTOM_BAR_COLOR = (193, 185, 174)  # 下色塊：莫蘭迪灰褐
TEXT_COLOR = 'white'  # 字體顏色

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920

# ───────────── 處理影片 ─────────────
def generate_vertical_video(term_folder,
                            english_line,
                            chinese_line):
    
    merged_video_path = os.path.join(term_folder, "merged_video.mp4")
    output_video_path = os.path.join(term_folder, "ig_shorts.mp4")


    clip = VideoFileClip(merged_video_path).with_fps(30)
    # 先將影片寬度縮放到 TARGET_WIDTH
    resized_clip = clip.resized(width=TARGET_WIDTH)
    VIDEO_HEIGHT = min(resized_clip.h, TARGET_HEIGHT)  # 影片高度不能超過畫布
    BAR_HEIGHT = (TARGET_HEIGHT - VIDEO_HEIGHT) // 2   # 動態計算色塊高度
    print(f"影片高度：{VIDEO_HEIGHT}，色塊高度：{BAR_HEIGHT}")
    # 以高度為 VIDEO_HEIGHT 置中裁剪
    y_start = max(0, (resized_clip.h - VIDEO_HEIGHT) // 2)
    y_end = y_start + VIDEO_HEIGHT
    cropped_clip = resized_clip.cropped(y1=y_start, y2=y_end)

    # 色塊
    top_bar = ColorClip(size=(TARGET_WIDTH, BAR_HEIGHT), color=TOP_BAR_COLOR).with_duration(cropped_clip.duration)
    bottom_bar = ColorClip(size=(TARGET_WIDTH, BAR_HEIGHT), color=BOTTOM_BAR_COLOR).with_duration(cropped_clip.duration)

    ## 上方文字
    font_size = 60
    margin = 40
    top_english_text_clip = (TextClip(
        text=english_line,
        font_size=font_size,
        color=TEXT_COLOR,
        font="Hiragino Sans GB.ttc",
        method="caption",
        size=(TARGET_WIDTH, BAR_HEIGHT)
    ).with_duration(cropped_clip.duration)
    .with_position(("center",  (BAR_HEIGHT // 2) - (font_size + margin)*2))
    )
    top_chinese_text_clip = (TextClip(
        text=chinese_line,
        font_size=font_size,
        color=TEXT_COLOR,
        font="Hiragino Sans GB.ttc",
        method="caption",
        size=(TARGET_WIDTH, BAR_HEIGHT)
    ).with_duration(cropped_clip.duration)
    .with_position(("center",  (BAR_HEIGHT // 2) - (font_size + margin)))
    )
    
    ## 下方文字
    bottom_text_clip = (TextClip(
        text=BOTTOM_TEXT,
        font_size=font_size,
        color=TEXT_COLOR,
        font="Hiragino Sans GB.ttc",
        method="caption",
        size=(TARGET_WIDTH, BAR_HEIGHT)
    ).with_duration(cropped_clip.duration)
    .with_position(("center",  (font_size + margin) - (BAR_HEIGHT // 2)))
    )

    # 合成
    top_composite = CompositeVideoClip(
        [top_bar, 
         top_english_text_clip, 
         top_chinese_text_clip]
         ).with_position(("center", 0))
    main_clip = cropped_clip.with_position(("center", BAR_HEIGHT))
    bottom_composite = CompositeVideoClip([bottom_bar, bottom_text_clip]).with_position(("center", BAR_HEIGHT + cropped_clip.h))

    # 合併所有片段
    final = CompositeVideoClip(
        [top_composite, main_clip, bottom_composite],
        size=(TARGET_WIDTH, TARGET_HEIGHT)
    )

    final.write_videofile(output_video_path,
                        codec="libx264", 
                        audio_codec="aac", 
                        threads=4, 
                        preset="medium",
                        bitrate="8M",
                        )

if __name__ == "__main__":
    term_folder = "downloads/its not about"
    english_line = "It's not about..."
    chinese_line = "這跟...無關。"
    generate_vertical_video(term_folder=term_folder,
                            english_line=english_line,
                            chinese_line=chinese_line)