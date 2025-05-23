from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip

# ───────────── 變數區 ─────────────

INPUT_PATH = "downloads/are you serious/merged_video.mp4"  # 輸入影片路徑
OUTPUT_PATH = "downloads/are you serious/ig_shorts.mp4"  # 輸出影片路徑

TOP_TEXT = "Are you serious?"  # 上方文字
BOTTOM_TEXT = "One quote a day"  # 下方文字

TOP_BAR_COLOR = (206, 198, 185)  # 上色塊：莫蘭迪灰粉
BOTTOM_BAR_COLOR = (193, 185, 174)  # 下色塊：莫蘭迪灰褐
TEXT_COLOR = 'white'  # 字體顏色

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920
BAR_HEIGHT = 240

# ───────────── 處理影片 ─────────────

def generate_vertical_video():
    clip = VideoFileClip(INPUT_PATH).with_fps(30)
    resized_clip = clip.resized(width=TARGET_WIDTH)
    max_video_height = TARGET_HEIGHT - 2 * BAR_HEIGHT  # 1440
    y_start = max(0, (resized_clip.h - max_video_height) // 2)
    y_end = y_start + max_video_height
    cropped_clip = resized_clip.cropped(y1=y_start, y2=y_end)

    # 色塊
    top_bar = ColorClip(size=(TARGET_WIDTH, BAR_HEIGHT), color=TOP_BAR_COLOR).with_duration(cropped_clip.duration)
    bottom_bar = ColorClip(size=(TARGET_WIDTH, BAR_HEIGHT), color=BOTTOM_BAR_COLOR).with_duration(cropped_clip.duration)

    # 文字
    top_text_clip = TextClip(
        text=TOP_TEXT,
        font_size=60,
        color=TEXT_COLOR,
        font="Arial.ttf",
        method="caption",
        size=(TARGET_WIDTH, BAR_HEIGHT)
    ).with_duration(cropped_clip.duration).with_position(("center", "center"))

    bottom_text_clip = TextClip(
        text=BOTTOM_TEXT,
        font_size=50,
        color=TEXT_COLOR,
        font="Arial.ttf",
        method="caption",
        size=(TARGET_WIDTH, BAR_HEIGHT)
    ).with_duration(cropped_clip.duration).with_position(("center", "center"))

    # 合成
    top_composite = CompositeVideoClip([top_bar, top_text_clip]).with_position((0, 0))
    main_clip = cropped_clip.with_position((0, BAR_HEIGHT))
    bottom_composite = CompositeVideoClip([bottom_bar, bottom_text_clip]).with_position((0, BAR_HEIGHT + cropped_clip.h))

    # 合併所有片段
    final = CompositeVideoClip(
        [top_composite, main_clip, bottom_composite],
        size=(TARGET_WIDTH, TARGET_HEIGHT)
    )

    final.write_videofile(OUTPUT_PATH, codec="libx264", audio_codec="aac", threads=4, preset="ultrafast")

if __name__ == "__main__":
    generate_vertical_video()