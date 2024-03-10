import os

from gpt import *
from video import *
from utils import *
from search import *
from uuid import uuid4
from tiktokvoice import *
from flask_cors import CORS
from termcolor import colored
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from moviepy.config import change_settings

import openai
from tools import *

# Load environment variables
load_dotenv("../.env")

# Set environment variables
SESSION_ID = os.getenv("TIKTOK_SESSION_ID")
change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Constants
HOST = "0.0.0.0"
PORT = 8082
AMOUNT_OF_STOCK_VIDEOS = 5
GENERATING = False


# Generation Endpoint
@app.route("/api/generate", methods=["POST"])
def generate():

    # Controllers
    eleven_controller = False
    add_music = True

    def pattern1(input_string, piece):
        pattern = re.escape(piece)
        match = re.search(pattern, input_string)
        if match:
            start_index = match.end() 
            following_text = input_string[start_index:] 
            return following_text
        else:
            return input_string

    def pattern2(input_string, piece):
        pattern = re.escape(piece)
        match = re.search(pattern, input_string)
        if match:
            end_index = match.start()  # Start of the match
            preceding_text = input_string[:end_index]  # Extract text preceding the pattern
            return preceding_text
        else:
            return input_string

    try:
        # Set global variable
        global GENERATING
        GENERATING = True

        # Clean
        clean_dir("../temp/")
        clean_dir("../subtitles/")

        # Parse JSON
        data = request.get_json()

        # Print little information about the video which is to be generated
        print(colored("[Video to be generated]", "blue"))
        print(colored("   Subject: " + data["videoSubject"], "blue"))

        if not GENERATING:
            return jsonify(
                {
                    "status": "error",
                    "message": "Video generation was cancelled.",
                    "data": [],
                }
            )

        # Generate a script
        # script = generate_script(data["videoSubject"])


        # The script is to be returned as a string.
        # Here is an example of a string:
        # "This is an example string."
       
        prompt = f"""
        Write a script for a 30-40 second video, based on this video description/subject: {data["videoSubject"]}

        Do not under any circumstance reference this prompt in your response.

        Get straight to the point, don't start with unnecessary things like, "welcome to this video".

        Obviously, the script should be related to the subject of the video.

        ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE.
        
        Keep the script to 3-4 sentances, this is for a youtube short, so make the script super interesting and concise! 

        
        Here is an example of what you might return, if the prompt was: Rocky Mountains
        You might return something like this: 

        The majestic Rocky Mountains, stretching across North America, are a breathtaking sight to behold
        With their towering peaks, stunning alpine lakes, and abundant wildlife, the Rockies offer unparalleled beauty and adventure
        Whether you're a hiker, skier, or simply a nature lover, the Rocky Mountains are a must-visit destination that will leave you in awe of the wonders of the natural world.

        
        Here is another example of what you might return, if the prompt was: Story about a polar bear
        You might return something like this: 
        
        In the vast expanse of the Arctic, a lone polar bear roams, its white coat blending seamlessly with the icy landscape. 
        With each step, it navigates the frozen terrain with grace and determination, its keen senses alert for any sign of prey. 
        As the endless winter sun bathes the scene in a soft glow, the polar bear's silent journey epitomizes the quiet strength and resilience of the Arctic wilderness.

        """
        script = get_message(prompt)
        print(script)



        # voice = data["voice"]
        # if not voice:
        #     print(colored("[!] No voice was selected. Defaulting to \"en_us_001\"", "yellow"))
        #     voice = "en_us_002"
        voice = "en_us_002"

        # Generate search terms
        list_prompt0 = f"""
        Generate {AMOUNT_OF_STOCK_VIDEOS} search terms for stock videos,
        depending on the subject of a video.
        Subject: {data["videoSubject"]}

        The search terms are to be returned as
        a JSON-Array of strings.

        Each search term should consist of 1-3 words,
        always add the main subject of the video.
        
        YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
        YOU MUST NOT RETURN ANYTHING ELSE. 
        YOU MUST NOT RETURN THE SCRIPT.
        
        The search terms must be related to the subject of the video.
        Here is an example of a JSON-Array of strings:
        ["search term 1", "search term 2", "search term 3"]

        For context, here is the full text:
        {script}
        """

        list_prompt = f"""
        Generate {AMOUNT_OF_STOCK_VIDEOS} search terms for stock videos, to put in a video about: {data["videoSubject"]}

        write a list starting at 1:
        Each search term should consist of 1-3 words,
        For context, here is the full text:
        {script}
        """

        search_terms = get_message(list_prompt)
        # print(search_terms)

        # Extract search terms
        terms = []
        try:
            for i in range(AMOUNT_OF_STOCK_VIDEOS):
                j=i+1
                search_idx = f"{j}."
                stop_idx = f"{j+1}."
                following_text = pattern1(search_terms, search_idx)
                current_item = ""
                if i < AMOUNT_OF_STOCK_VIDEOS - 1:
                    current_item = pattern2(following_text, stop_idx)
                else: current_item = following_text
                # print(current_item)
                terms.append(current_item.strip().replace('"', "").replace("'", ""))
        except Exception:
            exit()

        search_terms = terms
        print(search_terms)
        # search_terms = get_search_terms(
        #     data["videoSubject"], AMOUNT_OF_STOCK_VIDEOS, script
        # )


        # Search for a video of the given search term
        video_urls = []

        # Loop through all search terms,
        # and search for a video of the given search term
        for search_term in search_terms:
            if not GENERATING:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Video generation was cancelled.",
                        "data": [],
                    }
                )
            found_url = search_for_stock_videos(
                search_term, os.getenv("PEXELS_API_KEY")
            )

            if found_url != None and found_url not in video_urls and found_url != "":
                video_urls.append(found_url)

        # Define video_paths
        video_paths = []
        print(colored("[+] Downloading videos...", "blue"))

        # Save the videos
        for video_url in video_urls:
            if not GENERATING:
                return jsonify(
                    {
                        "status": "error",
                        "message": "Video generation was cancelled.",
                        "data": [],
                    }
                )
            try:
                saved_video_path = save_video(video_url)
                video_paths.append(saved_video_path)
            except Exception:
                print(colored(f"[-] Could not download video: {video_url}", "red"))

        print(colored("[+] Videos downloaded!", "green"))
        print(colored("[+] Script generated!\n", "green"))

        if not GENERATING:
            return jsonify(
                {
                    "status": "error",
                    "message": "Video generation was cancelled.",
                    "data": [],
                }
            )
        
        def gen_eleven_labs(path, script):
            import requests

            voice_id = "21m00Tcm4TlvDq8ikWAM"
            CHUNK_SIZE = 1024
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

            headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": os.getenv("ELEVEN_LABS_API_KEY2")
            }

            data = {
            "text": script,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
            }

            response = requests.post(url, json=data, headers=headers)
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

        paths = []
        # Generate TTS for every sentence
        # Split script into sentences
        sentences = script.split(". ")
        # Remove empty strings
        sentences = list(filter(lambda x: x != "", sentences))
        print(sentences)

        if eleven_controller: 
            if not GENERATING:
                return jsonify({
                        "status": "error",
                        "message": "Video generation was cancelled.",
                        "data": [],
                    })
            
            current_tts_path = f"../temp/{uuid4()}.mp3"
            print("Fetching voice over")

            try:
                gen_eleven_labs(current_tts_path, script)
            except Exception: 
                print("Failed getting voice over")
                exit()

            audio_clip = AudioFileClip(current_tts_path)
            paths.append(audio_clip)
        else: 
            for sentence in sentences:
                print("Sentance num: ", sentence)
                if not GENERATING:
                    return jsonify({
                            "status": "error",
                            "message": "Video generation was cancelled.",
                            "data": [],
                        })
                
                current_tts_path = f"../temp/{uuid4()}.mp3"
                print("Fetching voice over")
                tts(sentence, voice, filename=current_tts_path)

                audio_clip = AudioFileClip(current_tts_path)
                paths.append(audio_clip)

        print("Combining TTS files...")
        print("paths", len(paths))
        # Combine all TTS files using moviepy
        final_audio = concatenate_audioclips(paths)
        tts_path = f"../temp/{uuid4()}.mp3"
        final_audio.write_audiofile(tts_path)

        # Generate subtitles
        print("Generating subtitles...")
        subtitles_path = generate_subtitles(script, audio_path=tts_path, sentences=sentences, audio_clips=paths)

        # Concatenate videos
        temp_audio = AudioFileClip(tts_path)
        # combined_video_path = combine_videos(video_paths, temp_audio.duration)
        combined_video_array = combine_videos(video_paths, temp_audio.duration)
        print(combined_video_array)

        combined_video_path = combined_video_array[0]
        minHeight = combined_video_array[1]
        print("Passed Out of Range Error")

        # Handle music 
        newFileName = "music.mp4"
        newAudioName = "music.mp3"
        video_url = get_random_link()
        print(video_url)

        download_yt_video(video_url, newFileName)

        video_path = f"../temp/{newFileName}"
        audio_path = f"../temp/{newAudioName}"
        extract_audio(video_path, audio_path)

        new_length = temp_audio.duration
        print("Cutting audio to " + str(temp_audio.duration))
        cut_audio(audio_path, new_length, random_start=False)
  

        # Put everything together
        final_video_path = generate_video(combined_video_path, tts_path, subtitles_path, minHeight, audio_path)

        # Let user know
        print(colored(f"[+] Video generated: {final_video_path}!", "green"))

        # Stop FFMPEG processes
        if os.name == "nt":
            # Windows
            os.system("taskkill /f /im ffmpeg.exe")
        else:
            # Other OS
            os.system("pkill -f ffmpeg")

        GENERATING = False

        # Return JSON
        return jsonify(
            {
                "status": "success",
                "message": "Video generated! See temp/output.mp4 for result.",
                "data": final_video_path,
            }
        )
    except Exception as err:
        print(colored(f"[-] Error: {str(err)}", "red"))
        return jsonify(
            {
                "status": "error",
                "message": f"Could not retrieve stock videos: {str(err)}",
                "data": [],
            }
        )


@app.route("/api/cancel", methods=["POST"])
def cancel():
    print(colored("[!] Received cancellation request...", "yellow"))

    global GENERATING
    GENERATING = False

    return jsonify({"status": "success", "message": "Cancelled video generation."})
def check_file_permissions(video_path):
    if not os.access(video_path, os.R_OK):
        return False
    return True

@app.route('/api/video')
def get_video():
    video_path = "../temp/output1.mp4"

    # Check if the request includes a 'Range' header
    if 'Range' in request.headers:
        # Parse the byte range from the request header
        range_header = request.headers.get('Range')
        start, end = range_header.replace('bytes=', '').split('-')
        start = int(start)
        end = int(end) if end else None

        # Open the video file in binary mode
        with open(video_path, 'rb') as f:
            # Seek to the requested byte range
            f.seek(start)
            data = f.read(end - start + 1)

        # Set the appropriate response headers for the byte range
        status_code = 206  # Partial Content
        content_range = f'bytes {start}-{end}/{os.path.getsize(video_path)}'
        headers = {
            'Content-Range': content_range,
            'Accept-Ranges': 'bytes',
            'Content-Length': len(data),
            'Content-Type': 'video/mp4'
        }
        
        return data, status_code, headers
    else:
        # If no byte range is requested, serve the entire video file
        return send_file(video_path, mimetype='video/mp4')
    
    
# # def get_video():
#     video_relative_path = "../temp/output1.mp4"
#     # video_relative_path = "../temp/bec9d29b-6c8a-40ca-802d-09ee3d6cf512.mp4"
#     video_absolute_path = os.path.abspath(video_relative_path)

#     if not os.path.exists(video_absolute_path):
#         return "Video file not found", 404

#     if not check_file_permissions(video_absolute_path):
#         return "Insufficient permissions to access the video file", 403

#     try:
#         print("Sending video...")
#         return send_file(video_absolute_path, mimetype="video/mp4")
#     except Exception as e:
#         print(f"Error sending video: {e}")
#         return "Error sending video", 500

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
