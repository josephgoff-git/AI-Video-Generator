import requests

from typing import List
from termcolor import colored

def search_for_stock_videos(query: str, api_key: str) -> List[str]:
    """
    Searches for stock videos based on a query.

    Args:
        query (str): The query to search for.
        api_key (str): The API key to use.

    Returns:
        List[str]: A list of stock videos.
    """
    def get_video(query, api_key):
        # Build headers
        headers = {
            "Authorization": api_key
        }

        # Build URL
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=3"

        # Send the request
        r = requests.get(url, headers=headers)

        # Parse the response
        response = r.json()

        # Get first video url
        video_urls = []
        video_url = ""
        try:
            video_urls = response["videos"][0]["video_files"]
        except Exception:
            print(colored("[-] No Videos found.", "red"))
            print(colored(response, "red"))

        # Loop through video urls
        min_height = 900
        for video in video_urls:
            # Check if video has a download link
            if ".com/external" in video["link"] and video["height"] >= min_height and (video["width"]/video["height"]) >= 9/16:
                # Set video url
                video_url = video["link"]
                break

        # Let user know
        print(colored(f"\t=>{video_url}", "cyan"))

        # Return the video url
        return video_url

    video_url = get_video(query, api_key)

    while video_url == None or video_url == "":
        query = query.split(" ")
        if len(query) >= 2:
            query = " ".join(query[0:-1])
            video_url = get_video(query, api_key)
        else:
            if len(query) == 1: 
                query = query[0]
                video_url = get_video(query, api_key)
            break
    return video_url

