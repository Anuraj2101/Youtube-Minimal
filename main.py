import os, pickle, sqlite3
import googleapiclient.discovery
# from pyvidplayer2 import Video

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def search(cursor):
    search_string = str(input("Enter Your Search (0 to exit): "))
    search_results = search_table(cursor, search_string)
    
    cache = False
    if search_results == []:
        print("Not found in cache!")
        search_results=google_api_call(search_string)
    else:
        results_lst = []
        cache = True
        for tup in search_results:
           results_lst.append({tup[0]: tup[1]})
        search_results = results_lst

    link = menu(search_results, cursor, cache, search_string)
    return link 

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

def print_results(all_results):
    num = 0
    for result in all_results:
        num +=1
        print(f"{num}: {next(iter(result))} Link:{result[next(iter(result))]}")

def google_or_cache(results, cache, query):
    
    if cache == True:
        print(f"Printing {len(results)} results from Cache...")
        print_results(results)
        data_select = input("Would you like to pull results from the Google API instead? (Y/n):")
        if data_select == 'y':
            print("Hit!")
            results = google_api_call(query)
            print_results(results)
    print(results)
    return results

def menu(results, cursor, cache, query):
    results=google_or_cache(results, cache, query)
    
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

    if cache == False:
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
    print("Creating Table...")
    cursor.execute("CREATE TABLE IF NOT EXISTS links (title TEXT, link TEXT);") 

def search_table(cursor, string):
    db_results = cursor.execute(f"SELECT * FROM links where title LIKE '%{string}%';").fetchall()
    return db_results

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    
    conn = sqlite3.connect("Cache.db")
    cursor = conn.cursor()    
    create_table(cursor)

    link = search(cursor)
    print(link)
    cursor.execute("delete from links where rowid not in (select min(rowid) from links group by title, link);")
    conn.commit()
    
    

    #Video(link, youtube=True).preview()
if __name__ == "__main__":
    main()
    