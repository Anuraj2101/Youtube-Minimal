import yt_dlp, cv2, json
from google.cloud import secretmanager

URL='https://www.youtube.com/watch?v=MZpgzAizBNk'
PROJECT_ID = "fourth-cedar-435719-a6"
SECRET_ID = "account_password"
VERSION_NUM = 1
NAME = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/{VERSION_NUM}"

client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(request={"name": NAME})
password = response.payload.data.decode("UTF-8")

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {
    'username': 'oauth',
    'password': "",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    print(json.dumps(ydl.sanitize_info(info)))