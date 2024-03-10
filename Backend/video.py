import os
import uuid

import requests
import srt_equalizer
import assemblyai as aai

from typing import List
from moviepy.editor import *
from termcolor import colored
from dotenv import load_dotenv
from datetime import timedelta
# from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip

from moviepy.video.fx.resize import resize
from moviepy.editor import VideoFileClip
from openai import OpenAI

import subprocess

def convert_to_aac(input_path: str, output_path: str):
    """
    Convert audio file from MP3 to AAC format using FFmpeg.
    
    Args:
        input_path (str): Path to the input MP3 audio file.
        output_path (str): Path to save the output AAC audio file.
    """
    # Command to convert MP3 to AAC using FFmpeg
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ]

    try:
        # Execute FFmpeg command
        subprocess.run(command, check=True)
        print("Audio conversion completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio: {e}")
        raise


def optimize_video_for_web(input_path, output_path):
    """
    Re-encode and optimize a video file for web playback using FFmpeg.
    
    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the optimized output video file.
    """
    # Construct FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-tag:v", "hvc1",  # Add hvc1 tag
        "-movflags", "+faststart",
        output_path
    ]

    try:
        # Execute FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)
        print("Video optimization completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error optimizing video: {e}")
        raise




load_dotenv("../.env")

ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")

def save_video(video_url: str, directory: str = "../temp") -> str:
    """
    Saves a video from a given URL and returns the path to the video.

    Args:
        video_url (str): The URL of the video to save.
        directory (str): The path of the temporary directory to save the video to

    Returns:
        str: The path to the saved video.
    """
    video_id = uuid.uuid4()
    video_path = f"{directory}/{video_id}.mp4"
    with open(video_path, "wb") as f:
        f.write(requests.get(video_url).content)

    return video_path


def __generate_subtitles_assemblyai(audio_path: str) -> str:
    """
    Generates subtitles from a given audio file and returns the path to the subtitles.

    Args:
        audio_path (str): The path to the audio file to generate subtitles from.

    Returns:
        str: The generated subtitles
    """

    aai.settings.api_key = ASSEMBLY_AI_API_KEY
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    subtitles = transcript.export_subtitles_srt()

    return subtitles


def __generate_subtitles_locally(sentences: list[str], audio_clips: list[AudioFileClip]) -> str:
    """
    Generates subtitles from a given audio file and returns the path to the subtitles.

    Args:
        sentences (list[str]): all the sentences said out loud in the audio clips
        audio_clips (list[AudioFileClip]): all the individual audio clips which will make up the final audio track
    Returns:
        str: The generated subtitles
    """
    def convert_to_srt_time_format(total_seconds):
        # Convert total seconds to the SRT time format: HH:MM:SS,mmm
        if total_seconds == 0:
            return "0:00:00,0"
        # return str(timedelta(seconds=total_seconds))[:-3].replace('.', ',')
        return str(timedelta(seconds=total_seconds))[:-3]

    start_time = 0
    subtitles = []

    for i, (sentence, audio_clip) in enumerate(zip(sentences, audio_clips), start=1):
        duration = audio_clip.duration
        end_time = start_time + duration

        # Add slight delay
        # start_time += 2/5
        # end_time += 2/5
        # sentence = sentence.replace(',', '')

        # Format: subtitle index, start time --> end time, sentence
        subtitle_entry = f"{i}\n{convert_to_srt_time_format(start_time)} --> {convert_to_srt_time_format(end_time)}\n{sentence}\n"
        subtitles.append(subtitle_entry)

        start_time += duration  # Update start time for the next subtitle

    return "\n".join(subtitles)


def generate_subtitles(script: str, audio_path: str, sentences: list[str], audio_clips: list[AudioFileClip]) -> str:
    """
    Generates subtitles from a given audio file and returns the path to the subtitles.

    Args:
        audio_path (str): The path to the audio file to generate subtitles from.
        sentences (list[str]): all the sentences said out loud in the audio clips
        audio_clips (list[AudioFileClip]): all the individual audio clips which will make up the final audio track

    Returns:
        str: The path to the generated subtitles.
    """

    def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
        # Equalize subtitles
        srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)
    
    def compare_subs(script, text):
        return text
    
    subtitles_path = f"../subtitles/{uuid.uuid4()}.srt"

    if ASSEMBLY_AI_API_KEY is not None and ASSEMBLY_AI_API_KEY != "":
        print(colored("[+] Creating subtitles using AssemblyAI", "blue"))
        subtitles = __generate_subtitles_assemblyai(audio_path)
    else:
        print(colored("[+] Creating subtitles locally", "blue"))
        subtitles = __generate_subtitles_locally(sentences, audio_clips)



    # print(colored("[+] Creating subtitles with whisper", "blue"))
    # def make_subtitles(array):
    #     print(array)
    #     result = ""
    #     j = 1
    #     skip = False
    #     for i, item in enumerate(array): 
    #         if skip:
    #             skip = False
    #             continue
    #         def get_time(example):
    #             time = ""
    #             time_split = str(example).split(":")
    #             if len(time_split) > 1:
    #                 time += "00:"
    #                 minutes = time_split[len(time_split)-2]
    #                 if len(minutes) > 1:
    #                     time += minutes + ":"
    #                 else:
    #                     time += "0" + minutes + ":"
    #             else: 
    #                 time += "00:00:"

    #             seconds = time_split[len(time_split)-1]
    #             seconds_split = seconds.split(".")
    #             ms = seconds_split[1][0:3]
    #             seconds = seconds_split[0]
    #             if len(seconds) > 1:
    #                 time += seconds
    #             else:
    #                 time += "0" + seconds
    #             time += "," + ms
    #             return time

    #         start_time = get_time(array[i]['start'])
    #         end_time = get_time(array[i]['end'])

    #         word = array[i]['word']
    #         if i < len(array)-1:
    #             next_end_time = get_time(array[i+1]['end'])
    #             if end_time == next_end_time:
    #                 word += " " + array[i+1]['word']
    #                 skip = True
                    

    #         result += str(j) + "\n"
    #         result += start_time + " --> " + end_time + "\n"
    #         result += word + "\n"
    #         result += "\n"
    #         j += 1

    #     return result

    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # audio_file = open(audio_path, "rb")
    # transcript = client.audio.transcriptions.create(
    #     file=audio_file,
    #     model="whisper-1",
    #     response_format="verbose_json",
    #     timestamp_granularities=["word"],
    #     prompt = script
    # )

    # subtitles = make_subtitles(transcript.words)
    # print(subtitles)
        


    with open(subtitles_path, "w") as file:
        file.write(subtitles)

    # Equalize subtitles
    equalize_subtitles(subtitles_path)

    print(colored("[+] Subtitles generated.", "green"))

    return subtitles_path


def combine_videos(video_paths: List[str], max_duration: int) -> str:
    """
    Combines a list of videos into one video and returns the path to the combined video.

    Args:
        video_paths (list): A list of paths to the videos to combine.
        max_duration (int): The maximum duration of the combined video.

    Returns:
        str: The path to the combined video.
    """
    video_id = uuid.uuid4()
    combined_video_path = f"../temp/{video_id}.mp4"

    print(colored("[+] Combining videos...", "blue"))
    print(colored(f"[+] Each video will be {max_duration / len(video_paths)} seconds long.", "blue"))


    minHeight = 10000
    videoFiles = []
    for video_path in video_paths:
        clip = VideoFileClip(video_path)
        clip = clip.without_audio()
        clip = clip.subclip(0, max_duration / len(video_paths))
        clip = clip.set_fps(30)
        if clip.h < minHeight:
            minHeight = clip.h
        videoFiles.append(clip)
    
    print(minHeight)
    print(len(videoFiles))

    clips = []
    # i = 0
    for clip in videoFiles:
        try:
            print("Resizing")
            # i+=1
            # Resize based on minHeight
            print(clip.w, clip.h)
            ratio = minHeight / clip.h
            clip = clip.resize((int(clip.w * ratio), int(clip.h * ratio)))
            print("Resized", clip.w, clip.h)

            # Crop 
            # width = int(minHeight * 9/16)
            width = int(clip.h * 9/16)
            print("New width: ", width)
            crop_x = (clip.w - width) / 2
            clip = clip.crop(x1=crop_x, width=width)

            # Original mods
            # if not clip.h > clip.w:
            #     clip = crop(clip, width=1080, height=1920, \
            #                 x_center=clip.w / 2, \
            #                 y_center=clip.h / 2)
            # clip = clip.resize((1080, 1920))
            
            # path2 = f"../temp/video{i}.mp4"
            # clip2.write_videofile(path2, threads=3)

            clips.append(clip)
        except Exception:
            print("Error resizing images")
            print(Exception)


    print("Resized")

    print("clips:", len(clips))
    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_fps(30)
    final_clip.write_videofile(combined_video_path, threads=3)
    print("Created Video!")
    return [combined_video_path, minHeight]


def generate_video(combined_video_path: str, tts_path: str, subtitles_path: str, minHeight: int, audio_path: str) -> str:
    """
    This function creates the final video, with subtitles and audio.

    Args:
        combined_video_path (str): The path to the combined video.
        tts_path (str): The path to the text-to-speech audio.
        subtitles_path (str): The path to the subtitles.

    Returns:
        str: The path to the final video.
    """
    # Make a generator that returns a TextClip when called with consecutive
    print("Min height", minHeight)
    ratio = minHeight / 900
    generator = lambda txt: TextClip(
        txt,
        font="../fonts/bold_font.ttf",
        # fontsize=int(19 * ratio),
        fontsize=int(35 * ratio),
        color="white",
        stroke_color="black",
        stroke_width=int(1.8 * ratio),
    )

    # Burn the subtitles into the video
    print(colored("Burning Subtitles", "cyan"))
    subtitles = SubtitlesClip(subtitles_path, generator)
    result = CompositeVideoClip([
        VideoFileClip(combined_video_path),
        # subtitles.set_pos(("center", "center"))
        subtitles.set_pos(("center", minHeight * 3/4 - 10))
    ])
    
    try:
        print("Merging audio")
        from pydub import AudioSegment

        def merge_audio(subtitles_path, music_path, output_path):
            # Load audio files
            subtitles_audio = AudioSegment.from_file(subtitles_path)
            music_audio = AudioSegment.from_file(music_path)

            # Ensure both audio files have the same duration
            if len(subtitles_audio) > len(music_audio):
                subtitles_audio = subtitles_audio[:len(music_audio)]
            else:
                music_audio = music_audio[:len(subtitles_audio)]

            merged_audio = subtitles_audio.overlay(music_audio)
            merged_audio.export(output_path, format="mp3")
        
        print(tts_path)
        merge_audio(tts_path, "../temp/music.mp3", "../temp/output.mp3")
        # Example usage

        print("Trying to convert to AAC")
        convert_to_aac("../temp/output.mp3", "../temp/output.aac")
        # Example usage:

    except Exception: 
        print("Merge failed")
        exit()

    # Add the audio
    audio = AudioFileClip("../temp/output.aac")
    result = result.set_audio(audio)

 

    result.write_videofile("../temp/output.mp4", threads=3)
    print("optimizing")
    optimize_video_for_web("../temp/output.mp4", "../temp/output1.mp4")


    return "output.mp4"


