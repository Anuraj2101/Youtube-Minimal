import googleapiclient.discovery, pickle, os

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def google_api_call(search_string) -> list:
    api_service_name = "youtube"
    api_version = "v3"
    
    # with open("Youtube API Key.txt", "r") as f:
    #     DEVELOPER_KEY = f.readlines()
    if str(os.environ.get("ENVIRONMENT")) == "dev":
        DEVELOPER_KEY = str(os.environ.get("YOUTUBE_API_KEY"))
    elif str(os.environ.get("ENVIRONMENT")) == "local": 
        with open(str(os.environ.get("YOUTUBE_API_KEY")), "r") as f:
            DEVELOPER_KEY = f.readlines()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(

        part='snippet',
        maxResults=10,
        q = search_string,
        type = 'video'

    )

    response = request.execute()["items"]
    with open("Response.txt", "wb") as f:
        pickle.dump(str(response), f)
    
    return parse_results(response)

def parse_results(resp) -> list:
    cleaned_resp = []
    for item in resp:    
        if item["id"]["kind"] != "youtube#video":
            continue
        vid_id = item["id"]["videoId"]
        vid_name = item["snippet"]["title"]
        channel_id = item["snippet"]["channelTitle"]
        date_pub = item["snippet"]["publishTime"]
        cleaned_resp.append(clean_results(str(vid_name).replace("&quot;", "\""), vid_id))

    return cleaned_resp

def clean_results(video_name, video_id) -> list:
    
    return {video_name.encode('utf-8'):f"https://youtube.com/embed/{video_id}".encode('utf-8')}


# search_string = str(input("Enter Your Search: "))
# resp = google_api_call(search_string)
# print(resp)