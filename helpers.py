# def pattern3(input_string):
#     pattern = r'return \('
#     match = re.search(pattern, input_string)
#     if match:
#         start_index = match.end() 
#         following_text = input_string[start_index:] 
#         return following_text
#     else:
#         return input_string

# def pattern4(input_string):
#     pattern = r'\)\;*\s*\}\;*\s*export default'
#     match = re.search(pattern, input_string)
#     if match:
#         end_index = match.start()  # Start of the match
#         preceding_text = input_string[:end_index]  # Extract text preceding the pattern
#         return preceding_text
#     else:
#         return input_string





# def generate_script2(video_subject: str) -> str:
#     prompt = f"""
#     Write a script for a 30-40 second video, based on this subject: {video_subject}

#     The script is to be returned as a string.
#     Here is an example of a string:
#     "This is an example string."

#     Do not under any circumstance reference this prompt in your response.

#     Get straight to the point, don't start with unnecessary things like, "welcome to this video".

#     Obviously, the script should be related to the subject of the video.

#     ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE.

#     Keep the script to 3-4 sentences, this is for a youtube short, so make the script super interesting and concise!
#     """

#     # Set up OpenAI API key
#     api_key = os.environ.get("OPENAI_API_KEY")
#     openai.api_key = api_key

#     # Generate script
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo-instruct",  # You can adjust the engine as per your preference
#         prompt=prompt,
#         max_tokens=100,  # Adjust the token count based on your preference
#         temperature=0.7,  # Adjust the temperature as per your preference
#         stop="\n"  # Stop generation at new lines
#     )

#     # Return the generated script
#     if response:
#         print(response.choices[0].text.strip())
#         return response.choices[0].text.strip()
#     print("GPT-3.5 returned an empty response.")
#     return None
