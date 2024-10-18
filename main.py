import os, pickle, sqlite3
import googleapiclient.discovery
from pyvidplayer2 import Video

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def search():
    query = str(input("Enter Your Search (0 to exit): "))
    
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

def menu(results, cursor):
    num = 0
    for result in results:
        num +=1
        print(f"{num}: {next(iter(result))} Link:{result[next(iter(result))]}")
    
    while True:
        try:
            selection = int(input("Which Result Would You Like to Access? (0 to Exit): "))
        except Exception as e:
            print(e)
            continue

        if selection < 0 or selection > len(results):
            continue
        else:
            break
    title = list(results[selection - 1].keys())[0]
    link = results[selection - 1][next(iter(results[selection - 1]))]
    cursor.execute(f"INSERT INTO links VALUES ('{title}', '{link}');")

    if selection == 0:
        return None
    else:  
        return link

def google_api_call(search_string):
    api_service_name = "youtube"
    api_version = "v3"
    
    with open("Youtube API Key.txt", "r") as f:
        DEVELOPER_KEY = f.readlines()
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q = search_string
    )

    response = request.execute()["items"]
    return parse_results(response)

def create_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS links (title TEXT, link TEXT);") 

def search_table(cursor, string):
    db_results = cursor.execute(f"SELECT * FROM links where title LIKE '%{string}%';").fetchall()
    print(db_results)
    return db_results

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    
    conn = sqlite3.connect("Cache.db")
    cursor = conn.cursor()    
    create_table(cursor)

    search_string = search()
    search_results = search_table(cursor, search_string)
    if search_results == []:
        print("Not found in cache!")
        search_results=google_api_call(search_string)

    link=menu(search_results, cursor)
    print(link)
    with open("Response.txt", "wb") as f:
        pickle.dump(str(search_results), f)

    #Video(link, youtube=True).preview()
if __name__ == "__main__":
    main()