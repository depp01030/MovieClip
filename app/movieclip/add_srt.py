import os
import whisper

#%%
def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace('.', ',')

def create_srt_for_video(video_path):
    """
    使用 Whisper 模型將視頻轉換為 SRT 字幕文件
    :param video_path: 視頻文件路徑
    :param srt_path: 輸出 SRT 文件路徑
    """ 
    try:
        model = whisper.load_model("base")  # 可選 tiny, base, small, medium, large
        result = model.transcribe(video_path)


        srt_path = video_path.replace(".mp4", ".srt")  # 假設視頻是 mp4 格式

        # 儲存為 SRT 字幕
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()

                f.write(f"{i+1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")
        return srt_path
    except Exception as e:
        print(f"❌ 錯誤：{e}")
        return None
def create_srt_for_folder(term_folder):

    for filename in os.listdir(term_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(term_folder, filename)

            srt_path = create_srt_for_video(video_path = video_path)
             
            if not os.path.exists(srt_path):
                print(f"🎬 轉換 {video_path} 為 SRT 字幕")
                # create_srt(video_path)  # Uncomment this line to create SRT files
            else:
                print(f"✅ 已存在字幕檔：{srt_path}")
    
if __name__ == "__main__":
    video_path = "downloads/i am surprised/1.mp4"  # 替換為你的視頻文件路徑
    term_folder = "downloads/i am surprised"  # 替換為你的視頻文件夾路徑
    # create_srt_for_video(video_path)
    create_srt_for_folder(term_folder)