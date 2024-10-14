# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os, pickle
import googleapiclient.discovery
from pyvidplayer2 import Video

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    
    with open("Youtube API Key.txt", "r") as f:
        DEVELOPER_KEY = f.readlines()
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q = "Marc Brunet"
    )
    response = request.execute()["items"]
    for item in response:
        for key in item: 
            print(key, item[key])
    with open("Response.txt", "wb") as f:
        pickle.dump(str(response), f)

    Video("https://www.youtube.com/watch?v=-EFmkxC8eBo", youtube=True).preview()
if __name__ == "__main__":
    main()