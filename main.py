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
        vid_id = item["id"]["videoId"]
        vid_name = item["snippet"]["title"]
        cleaned_resp.append(clean_results(str(vid_name).replace("&quot;", "\""), vid_id))

    return cleaned_resp

def clean_results(video_name, video_id):
    
    return {video_name:f"https://youtube.com/watch?v={video_id}"}

def menu(results):
    num = 0
    for result in results:
        num +=1
        print(f"{num}: {next(iter(result))} Link:{result[next(iter(result))]}")
    
    while True:
        try:
            selection = int(input("Which Search Would You Like to Access? (0 to Exit): "))
        except Exception as e:
            print(e)
            continue

        if selection < 0 or selection > len(results):
            continue
        else:
            break 

    if selection == 0:
        return None
    else:  
        return (results[selection - 1][next(iter(results[selection - 1]))])

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
    
    link=menu(search_results)
    print(link)

    with open("Response.txt", "wb") as f:
        pickle.dump(str(response), f)

    #Video(link, youtube=True).preview()
if __name__ == "__main__":
    query = search()
    main(query)