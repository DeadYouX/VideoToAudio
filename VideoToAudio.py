import os
import datetime
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def get_current_date_folder():
    current_date = datetime.datetime.now().strftime("%d_%m_%Y")
    return os.path.join("assets", current_date)

def check_completed(file_name):
    completed_dir = "completed"
    completed_file = os.path.join(completed_dir, file_name)
    return os.path.exists(completed_file)

def repeat_video_to_match_audio(video_clip, audio_duration):
    repeated_clips = []
    current_duration = 0

    while current_duration < audio_duration:
        repeated_clips.append(video_clip)
        current_duration += video_clip.duration

    final_video = concatenate_videoclips(repeated_clips)
    return final_video.subclip(0, audio_duration)

def add_fade_effects(clip, fade_duration=1):
    faded_clip = clip.fadein(fade_duration).fadeout(fade_duration)
    return faded_clip

def process_files_in_folder(folder_path):
    completed_dir = "completed"
    os.makedirs(completed_dir, exist_ok=True)

    files = sorted(os.listdir(folder_path))
    video_files = [f for f in files if f.endswith(".mp4")]
    audio_files = [f for f in files if f.endswith(".mp3")]

    for i, video_file in enumerate(video_files, start=1):
        video_path = os.path.join(folder_path, video_file)
        audio_path = os.path.join(folder_path, audio_files[i-1])

        output_file_name = f"{os.path.basename(folder_path)}_{i}.mp4"
        output_file_path = os.path.join(completed_dir, output_file_name)

        if check_completed(output_file_name):
            print(f"{output_file_name} уже существует. Пропускаем...")
            continue

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        final_video_clip = repeat_video_to_match_audio(video_clip, audio_clip.duration)
        final_video_clip = add_fade_effects(final_video_clip, fade_duration=1)
        
        final_clip = final_video_clip.set_audio(audio_clip)

        final_clip.write_videofile(output_file_path, codec="libx264", audio_codec="aac")
        print(f"Создан: {output_file_name}")

        video_clip.close()
        audio_clip.close()

if __name__ == "__main__":
    date_folder = get_current_date_folder()
    if os.path.exists(date_folder):
        process_files_in_folder(date_folder)
    else:
        print(f"Папка с текущей датой не найдена: {date_folder}")
