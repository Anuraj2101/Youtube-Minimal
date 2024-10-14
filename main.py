# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os, pickle
import googleapiclient.discovery
from pyvidplayer2 import Video

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def search():
    query = str(input("Search: "))
    return query

def parse_results(resp):
    cleaned_resp = []
    for item in resp:    
        if item["id"]["kind"] != "youtube#video":
            continue
        for key in item:
            vid_id = item["id"]["videoId"]
            vid_name = item["snippet"]["title"]
            cleaned_resp.append(clean_results(vid_name, vid_id))
            # print("Key:", key, "Value:", item[key])
    return cleaned_resp

def clean_results(video_name, video_id):
    
    return {video_name:f"https://youtube.com/watch?v={video_id}"}


def main(search_string):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    
    with open("Youtube API Key.txt", "r") as f:
        DEVELOPER_KEY = f.readlines()
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q = search_string
    )

    response = request.execute()["items"]
    search_results = parse_results(response)
    
    print(search_results)

    with open("Response.txt", "wb") as f:
        pickle.dump(str(response), f)

    #Video("https://www.youtube.com/watch?v=-EFmkxC8eBo", youtube=True).preview()
if __name__ == "__main__":
    query = search()
    main(query)