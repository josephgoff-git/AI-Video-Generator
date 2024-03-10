# import re
# from fuzzywuzzy import fuzz

# def count_words(text):
#     # Remove hyphens and replace them with spaces
#     text = text.replace('-', ' ')
#     # Count words
#     words = re.findall(r'\b\w+\b', text)
#     return len(words)

# def find_division_indices(original_script, divided_script):
#     division_indices = []
#     original_script_copy = original_script.lower()  # Convert to lowercase for case insensitivity

#     for substring in divided_script:
#         max_ratio = -1
#         best_match_index = -1

#         # Iterate through original script to find best match for current substring
#         for i in range(len(original_script) - len(substring) + 1):
#             match_ratio = fuzz.ratio(original_script_copy[i:i+len(substring)].lower(), substring.lower())
#             if match_ratio > max_ratio:
#                 max_ratio = match_ratio
#                 best_match_index = i

#         division_indices.append(best_match_index)

#     return division_indices

# def divide_script(original_script, division_indices):
#     # Get words from original script
#     original_words = re.findall(r'\b\w+\b', original_script)

#     # Initialize variables
#     substrings = []
#     start_index = 0

#     # Iterate through division indices
#     for index in division_indices:
#         # Get the number of words in the substring
#         num_words = count_words(original_script[start_index:index])

#         # Add the substring to the list
#         substrings.append(' '.join(original_words[start_index:start_index+num_words]))

#         # Update the start index
#         start_index += num_words

#     # Add the remaining part of the original script as the last substring
#     substrings.append(' '.join(original_words[start_index:]))

#     return substrings

# # Test
# original_script = "Money makes the world go round. It's a universal language that drives economies, fuels innovation, and empowers individuals. From the ancient bartering system to the digital era of cryptocurrencies, money has evolved and shaped human civilization. It can bring joy and comfort, but also stress and inequality. So, let's explore the fascinating world of money and its impact on our lives."
# divided_script = ["Money makes the world go round. It's a universal lan",
#                   "that drives economies, fuels innovation and empowers",
#                   "hindividuals. From the ancient bartering system to the digital area",
#                   "of cryptocurrencies, money has evolved and shaped human",
#                   "civilization. It can bring joy and comfort, but also",
#                   "stress and inequality. So let's explore the fascinating",
#                   "world-of money and its impact on our lives."]

# division_indices = find_division_indices(original_script, divided_script)
# substrings = divide_script(original_script, division_indices)

# print("Substrings:")
# for substring in substrings:
#     print()
#     print(substring)






# texts = [
#     "Twitter connect and share your thoughts news and ideas fit|",
#     "theworld in real time Follow your favorite influencers|",
#     "stay updated on trends and engage with a community that is is|",
#     "always buzzing With its concise format and ease|",
#     "of use Twitter is the go to platform for breaking knews|",
#     "live updates and meaningful conversaltions|",
#     "Done miss out on what's happening right now Join Twitter today|",
#     "and be part of the global conversation|",
# ]

# script = "Twitter: Connect and share your thoughts, news, and ideas with the world in real time. Follow your favorite influencers, stay updated on trends, and engage with a community that's always buzzing. With its concise format and ease of use, Twitter is the go-to platform for breaking news, live updates, and meaningful conversations. Don't miss out on what's happening right now. Join Twitter today and be part of the global conversation."

# def find_divisions(script, texts):
#     text = " ".join(texts)[:-1]

# find_divisions(script, texts)



# texts = [
#     "Twitter connect and share your thoughts news and ideas fit|",
#     "theworld in real time Follow your favorite influencers|",
#     "stay updated on trends and engage with a community that is is|",
#     "always buzzing With its concise format and ease|",
#     "of use Twitter is the go to platform for breaking knews|",
#     "live updates and meaningful conversaltions|",
#     "Done miss out on what's happening now Join Twitter today|",
#     "and be part of the global conversation|",
# ]

# corrected_text = " ".join(texts)



# divisions = "Twitter connect and share your thoughts news and ideas fit| theworld in real time Follow your favorite influencers| stay updated on trends and engage with a community that is is| always buzzing With its concise format and ease| of use Twitter is the go to platform for breaking knews| live updates and meaningful conversaltions| Done miss out on what's happening now Join Twitter today| and be part of the global conversation",
# script = "Twitter: Connect and share your thoughts, news, and ideas with the world in real time. Follow your favorite influencers, stay updated on trends, and engage with a community that's always buzzing. With its concise format and ease of use, Twitter is the go-to platform for breaking news, live updates, and meaningful conversations. Don't miss out on what's happening right now. Join Twitter today and be part of the global conversation."

# def find_divisions(script, divisions):
#     return None

# find_divisions(script, divisions)


# import re

# def remove_punctuation(text):
#     # Remove punctuation marks
#     return re.sub(r'[.,:;\'\"?\>\<\+\=\*\&\%\$\@\(\)\/\\\#\!\^\_\{\}\[\]]', '', text)

# def split_into_words(script):
#     # Remove punctuation marks and split the script into words
#     clean_script = remove_punctuation(script)
#     clean_script = clean_script.split(" ")
#     for i in range(len(clean_script)):
#         clean_script[i] = clean_script[i].lower()
#     return clean_script

# def find_divisions(correct_script, bugged_script):
#     correct_words = split_into_words(correct_script)
#     bugged_words = split_into_words(bugged_script)
    
#     print(correct_words)
#     print(bugged_words)

#     divisions_positions = []
#     return ""


# # Define the scripts
# divisions = "Twitter connect and share your thoughts news and ideas fit | theworld in real time Follow your favorite influencers | stay updated on trends and engage with a community that is is | always buzzing With its concise format and ease | of use Twitter is the go to platform for breaking knews | live updates and meaningful conversaltions | Done miss out on what's happening now Join Twitter today | and be part of the global conversation"
# correct_script = "Twitter: Connect and share your thoughts, news, and ideas with the world in real time. Follow your favorite influencers, stay updated on trends, and engage with a community that's always buzzing. With its concise format and ease of use, Twitter is the go-to platform for breaking news, live updates, and meaningful conversations. Don't miss out on what's happening right now. Join Twitter today and be part of the global conversation."

# # Find divisions
# divisions_positions = find_divisions(correct_script, divisions)
# print(divisions_positions)


# def find_indexes(script1, script2):
#     markers = []
#     index = 0
#     while index < len(script1) and index < len(script2):
#         if script1[index] != script2[index]:
#             if script2[index] == '|':
#                 markers.append(index)
#                 index += 1
#             index += 1
#         else:
#             index += 1
#     return markers

# script1 = ['twitter', 'connect', 'and', 'share', 'your', 'thoughts', 'news', 'and', 'ideas', 'with', 'the', 'world', 'in', 'real', 'time', 'follow', 'your', 'favorite', 'influencers', 'stay', 'updated', 'on', 'trends', 'and', 'engage', 'with', 'a', 'community', 'thats', 'always', 'buzzing', 'with', 'its', 'concise', 'format', 'and', 'ease', 'of', 'use', 'twitter', 'is', 'the', 'go-to', 'platform', 'for', 'breaking', 'news', 'live', 'updates', 'and', 'meaningful', 'conversations', 'dont', 'miss', 'out', 'on', 'whats', 'happening', 'right', 'now', 'join', 'twitter', 'today', 'and', 'be', 'part', 'of', 'the', 'global', 'conversation']
# script2 = ['twitter', 'connect', 'and', 'share', 'your', 'thoughts', 'news', 'and', 'ideas', 'fit', '|', 'theworld', 'in', 'real', 'time', 'follow', 'your', 'favorite', 'influencers', '|', 'stay', 'updated', 'on', 'trends', 'and', 'engage', 'with', 'a', 'community', 'that', 'is', 'is', '|', 'always', 'buzzing', 'with', 'its', 'concise', 'format', 'and', 'ease', '|', 'of', 'use', 'twitter', 'is', 'the', 'go', 'to', 'platform', 'for', 'breaking', 'knews', '|', 'live', 'updates', 'and', 'meaningful', 'conversaltions', '|', 'done', 'miss', 'out', 'on', 'whats', 'happening', 'now', 'join', 'twitter', 'today', '|', 'and', 'be', 'part', 'of', 'the', 'global', 'conversation']

# print(find_indexes(script1, script2))


# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()

# def make_subtitles(array):
#     result = ""
#     for i, item in enumerate(array): 
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

#         result += str(i+1) + "\n"
#         result += start_time + " --> " + end_time + "\n"
#         result += array[i]['word'] + "\n"
#         result += "\n"

#     return result

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# script = "Comma AI the future of self driving cars is here. Experience a new level of safety and convenience with Comma AI's Advanced Driver Assistance System. Say goodbye to the constant stress of driving and let our technology take the wheel. Upgrade your why today and join the revolution of autonomous vehicles with Comma AI"
# audio_file = open("../temp/8464e162-6b9a-49eb-aef9-d9e739610ec6.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   file=audio_file,
#   model="whisper-1",
#   response_format="verbose_json",
#   timestamp_granularities=["word"],
#   prompt = script
# )

# result = make_subtitles(transcript.words)
# print(result)


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
    print(response)

get_message("write a script for a movie trailer about king kong, and make it 30 seconds long")


