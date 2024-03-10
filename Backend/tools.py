from pytube import YouTube
import os
import random

minecraft_videos= [
    "https://www.youtube.com/watch?v=u7kdVe8q5zs"
]

# Playlist 1: https://www.youtube.com/watch?v=8IWuEiIBdwc&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=31
lofi_music = [
    "https://www.youtube.com/watch?v=BH-SnQ8J1VU&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg",
    "https://www.youtube.com/watch?v=GNCtaWIhdvM&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=2&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=dfrgjD-_hE4&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=3&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=GXYN8kATnVA&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=4&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=eJ-LvX9HLrU&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=5&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=6ukEy6FOxZE&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=6&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=Fs2kNf7nyE4&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=7&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=Q7HjxOAU5Kc&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=8&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=szd2Hg1BuQI&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=9&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=wnOoqdcf7zU&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=10&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=rfdcdV8Rlg8&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=11&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=lqUMNCRS3p4&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=12&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=DisZeyftY5I&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=13&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=VZkFJAb_gx4&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=14&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=powKEGuPvjc&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=18&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=Ig2LiJBriR4&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=19&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=C11iclSJTNA&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=20&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=znarNyPELcU&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=21&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=n_Ostub3y90&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=22&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=cTMOQiY0axo&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=23&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=twpQogWOgAs&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=24&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=-jrh3Mk8ZCA&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=25&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=yGI_nGCl76c&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=28&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=ZLfs029IywI&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=30&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=8IWuEiIBdwc&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=31&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=5aOBYaHgmk8&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=32&pp=iAQB8AUB",
    "https://www.youtube.com/watch?v=vOqge0pZypo&list=PLfP6i5T0-DkIMLNRwmJpRBs4PJvxfgwBg&index=36&pp=iAQB8AUB",
]   

pop_music_vocals = [
    "https://www.youtube.com/watch?v=jAnE_mH5tqo&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=1&pp=iAQB",
]

chill_pop = [
    "https://www.youtube.com/watch?v=6HjYZctMgEU&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=6&pp=iAQB",
]

pop_music = [
    "https://www.youtube.com/watch?v=D0kQ5OWcEYM&list=PLmurGgZIgor5rK6E9wg-I3ikqqTAaPnAs&index=1&pp=iAQB",
    "https://www.youtube.com/watch?v=kBgsZ-iTGHs&list=PLmurGgZIgor5rK6E9wg-I3ikqqTAaPnAs&index=6&pp=iAQB",
    "https://www.youtube.com/watch?v=rBG-z-vtZfI&list=PLmurGgZIgor5rK6E9wg-I3ikqqTAaPnAs&index=8",
    "https://www.youtube.com/watch?v=NU5G781QXRM&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=2&pp=iAQB",
    "https://www.youtube.com/watch?v=U2-o_q4WhAY&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=3",
    "https://www.youtube.com/watch?v=0V0z9p-3ims&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=5&pp=iAQB",
    "https://www.youtube.com/watch?v=6HjYZctMgEU&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=6&pp=iAQB",
    "https://www.youtube.com/watch?v=aMK_lLTDJHg&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=8",
    "https://www.youtube.com/watch?v=DZ4Cuu5O-2k&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=9",
    "https://www.youtube.com/watch?v=fCMaqC-GANk&list=PLxtj0Fzm7DkhZ4tctTtDN99NM9DwXsBF0&index=14",
]

def get_random_link():
    return pop_music[random.randint(0, len(pop_music))]

# Download Video from Youtube
def download_yt_video(video_url, name):
    yt = YouTube(video_url)
    video_stream = yt.streams.get_highest_resolution()
    download_dir = "../temp"
    os.makedirs(download_dir, exist_ok=True)  
    file_path = os.path.join(download_dir, name)
    video_stream.download(download_dir)
    default_filename = video_stream.default_filename
    os.rename(os.path.join(download_dir, default_filename), file_path)


# Download Audio from Video
from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_path)

        video_clip.close()
        audio_clip.close()
    except Exception as e:
        print(f"Error: {e}")


# Clip Audio Length
from pydub import AudioSegment
from pydub.utils import which
import random

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def cut_audio(audio_path, newLength, random_start):
    audio = AudioSegment.from_file(audio_path)
    newLength *= 1000
    start = 0
    if len(audio) > newLength: 
        if random_start: 
            start = random.randint(0, len(audio) - newLength)
        trimmed_audio = audio[start:newLength+start] 
        
        # Change volume
        trimmed_audio -= 20

        trimmed_audio.export(audio_path, format="mp3") 
        print("Audio trimmed and saved successfully.")
    else:
        print(f"Audio clip is already {newLength / 1000} seconds or shorter.")



def cut_video(video_path, new_duration, random_start):
    video = VideoFileClip(video_path)
    new_duration *= 1000  
    start = 0

    if (video.duration * 1000) > new_duration:
        # if random_start:
        #     start = random.randint(0, (video.duration * 1000) - new_duration)
        print(new_duration)
        print(video.duration * 1000)
        # clipped_video = video.subclip(start / 1000, (start + new_duration) / 1000)
        clipped_video = video.subclip(start, (start + new_duration) / 1000)
        clipped_video.write_videofile(video_path, codec='libx264', audio_codec='aac')
        print("Video clipped and saved successfully.")
    else:
        print(f"Video clip is already {new_duration / 1000} seconds or shorter.")

def cut_video2(video_path, new_duration, random_start):
    video = VideoFileClip(video_path)
    new_duration *= 1000  
    start = 0

    if (video.duration * 1000) > new_duration:
        # if random_start:
        #     start = random.randint(0, (video.duration * 1000) - new_duration)
        # clipped_video = video.subclip(start / 1000, (start + new_duration) / 1000)
        clipped_video = video.subclip(start, start + new_duration)
        clipped_video.write_videofile(video_path, codec='libx264', audio_codec='aac')
        print("Video clipped and saved successfully.")
    else:
        print(f"Video clip is already {new_duration / 1000} seconds or shorter.")


# # Run Functions
# newFileName = "file.mp4"
# newAudioName = "file_audio.mp3"
# video_url = """
# https://www.youtube.com/watch?v=RnzE6g-Czgs&list=PLC1og_v3eb4jE0bmdkWtizrSQ4zt86-3D
# """

# download_yt_video(video_url, newFileName)

# video_path = f"../temp/{newFileName}"
# audio_path = f"../temp/{newAudioName}"
# extract_audio(video_path, audio_path)

# new_length = 30
# cut_audio(audio_path, new_length, random_start=False)
# cut_video(video_path, new_length, random_start=False)
        
