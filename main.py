from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
import sys

# Le fichier JSON que vous avez téléchargé à partir de votre projet Google Cloud Console
CLIENT_SECRETS_FILE = "client_secrets.json"

# Cette variable définit les autorisations que votre application demande aux utilisateurs
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def initialize_upload(youtube, file):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "My video title",
                "description": "This is a description of my video",
                "tags": ["python", "youtube"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
    )
    return request

def upload_file(file):
    youtube = get_authenticated_service()
    initialize_upload(youtube, file)

# Supposons que vous avez une liste de fichiers mp4 dans le répertoire "videos"
import os

video_files = [f for f in os.listdir("videos") if f.endswith(".mp4")]

for video_file in video_files:
    try:
        upload_file(os.path.join("videos", video_file))
        print(f"Uploaded {video_file}")
    except HttpError as e:
        print(f"An error occurred: {e}")
        #caca