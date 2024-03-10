import re
import json
import g4f
from typing import List
from termcolor import colored

import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
client.api_key=os.getenv("OPENAI_API_KEY")

def get_message(user_msg):
    client = OpenAI()
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=user_msg,
        temperature=0.9,
        max_tokens=2000,
    )
    response = completion.choices[0].text
    print(colored(response, "cyan"))

    # import openai
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # system_msg = 'You are a helpful assistant who writes 30 second scripts for youtube short videos. you only return raw scripts, nothing else. '
    # response = client.ChatCompletions.create(
    #     model="gpt-3.5-turbo",
    #     temperature=0.9,
    #     # messages=[
    #     #     {"role": "system", "content": system_msg},
    #     #     {"role": "user", "content": user_msg}
    #     # ]
    #     )
    # response = response.choices[0].message.content.strip()
    # print(colored(response, "cyan"))

    if response:
        response = response.replace("*", "")
        response = response.replace("#", "")

        # Remove markdown syntax
        response = re.sub(r'\[.*\]', '', response)
        response = re.sub(r'\(.*\)', '', response)
        return f"{response} "


# def generate_script(video_subject: str) -> str:
#     prompt = f"""
#     Write a script for a 30-40 second video, based on this subject: {video_subject}

#     The script is to be returned as a string.
#     Here is an example of a string:
#     "This is an example string."

#     Do not under any circumstance reference this prompt in your response.

#     Get straight to the point, don't start with unnecessary things like, "welcome to this video".

#     Obviously, the script should be related to the subject of the video.

#     ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE.
    
#     Keep the script to 3-4 sentances, this is for a youtube short, so make the script super interesting and concise! 
#     """

#     # Generate script
#     response = g4f.ChatCompletion.create(
#         model=g4f.models.gpt_35_turbo_16k_0613,
#         messages=[{"role": "user", "content": prompt}],
#     )

#     print(colored(response, "cyan"))

#     # Return the generated script
#     if response:
#         # Clean the script
#         # Remove asterisks, hashes
#         response = response.replace("*", "")
#         response = response.replace("#", "")

#         # Remove markdown syntax
#         response = re.sub(r'\[.*\]', '', response)
#         response = re.sub(r'\(.*\)', '', response)

#         return f"{response} "
#     print(colored("[-] GPT returned an empty response.", "red"))
#     return None


# def get_search_terms(video_subject: str, amount: int, script: str) -> List[str]:
#     """
#     Generate a JSON-Array of search terms for stock videos,
#     depending on the subject of a video.

#     Args:
#         video_subject (str): The subject of the video.
#         amount (int): The amount of search terms to generate.
#         script (str): The script of the video.

#     Returns:
#         List[str]: The search terms for the video subject.
#     """

    # Build prompt
    # prompt = f"""
    # Generate {amount} search terms for stock videos,
    # depending on the subject of a video.
    # Subject: {video_subject}

    # The search terms are to be returned as
    # a JSON-Array of strings.

    # Each search term should consist of 1-3 words,
    # always add the main subject of the video.
    
    # YOU MUST ONLY RETURN THE JSON-ARRAY OF STRINGS.
    # YOU MUST NOT RETURN ANYTHING ELSE. 
    # YOU MUST NOT RETURN THE SCRIPT.
    
    # The search terms must be related to the subject of the video.
    # Here is an example of a JSON-Array of strings:
    # ["search term 1", "search term 2", "search term 3"]

    # For context, here is the full text:
    # {script}
    # """

    # Generate search terms
    # response = ""
    # try: 
    #     response = g4f.ChatCompletion.create(
    #         model=g4f.models.gpt_35_turbo_16k_0613,
    #         messages=[{"role": "user", "content": prompt}],
    #     )
    # except Exception: 
    #     print("error")
    #     exit()

    # Load response into JSON-Array
    # try:
    #     search_terms = json.loads(response)
    # except Exception:
    #     print(colored("[*] GPT returned an unformatted response. Attempting to clean...", "yellow"))
    #     print(response)
    #     # Use Regex to extract the array from the markdown
    #     search_terms = re.findall(r'\[.*\]', str(response))
    #     print()
    #     print(search_terms)
    #     if not search_terms:
    #         print(colored("[-] Could not parse response.", "red"))

    #     # Load the array into a JSON-Array
    #     search_terms = json.loads(search_terms)

    # Let user know
    # print(colored(f"\nGenerated {amount} search terms: {', '.join(search_terms)}", "cyan"))

    # Return search terms
    # search_terms = ["white mountains", "rocky mountains", "snow caps", "yellowstone", "skiing"]
    # return search_terms
