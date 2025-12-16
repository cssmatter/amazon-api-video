
import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import video_config

# Scopes required for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    """Authenticates the user and returns the YouTube API service."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("client_secrets.json"):
                print("Error: client_secrets.json not found.")
                print("Please download your OAuth 2.0 Client Credentials from Google Cloud Console")
                print("and save them as 'client_secrets.json' in this directory.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, file_path, title, description, category_id="22", privacy_status="private"):
    """
    Uploads a video to YouTube.
    
    Args:
        youtube: YouTube API service instance.
        file_path (str): Path to the video file.
        title (str): Video title.
        description (str): Video description.
        category_id (str): Video category ID (22 is usually People & Blogs, 24 is Entertainment).
        privacy_status (str): "private", "public", or "unlisted".
    """
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["amazon deals", "discounts", "shopping", "best buy"],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        }
    }

    print(f"Uploading {file_path}...")
    
    media = MediaFileUpload(
        file_path, 
        chunksize=-1, 
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload Complete!")
    print(f"Video ID: {response.get('id')}")
    print(f"Watch URL: https://www.youtube.com/watch?v={response.get('id')}")
    return response.get('id')

def add_video_to_playlist(youtube, video_id, playlist_id):
    """
    Adds a video to a specific playlist.
    
    Args:
        youtube: YouTube API service instance.
        video_id (str): ID of the video to add.
        playlist_id (str): ID of the playlist to add the video to.
    """
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print(f"Successfully added video {video_id} to playlist {playlist_id}")
    except Exception as e:
        print(f"Error adding video to playlist: {e}")

if __name__ == "__main__":
    youtube_service = authenticate_youtube()
    
    if youtube_service:
        video_file = video_config.OUTPUT_FILENAME
        
        if not os.path.exists(video_file):
            print(f"Error: Video file '{video_file}' not found.")
            exit(1)
            
        today_date = datetime.now().strftime("%Y-%m-%d")
        video_title = f"Today Top Amazon Deals - {today_date} #Amazon #AmazonOffers"
        
        # Load deals to create description
        try:
            with open("products.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                products = data.get("products", [])
        except Exception as e:
            print(f"Warning: Could not read products.json: {e}")
            products = []

        # Build description
        description_parts = [
            f"Check out today's best Amazon deals! ({today_date})",
            "",
            "Prices and availability are subject to change.",
            "As an Amazon Associate I earn from qualifying purchases.",
            "",
            "🔥 TODAY'S DEALS 🔥",
            ""
        ]

        for i, product in enumerate(products, 1):
            title = product.get("title", "Amazon Deal")
            link = product.get("product_url", "")
            if link:
                description_parts.append(f"{i}. {title}")
                description_parts.append(f"{link}")
                description_parts.append("")  # Empty line between products

        description_parts.append("#AmazonDeals #Shopping #Discounts")
        
        video_description = "\n".join(description_parts)
        
        video_description = "\n".join(description_parts)
        
        uploaded_video_id = upload_video(
            youtube_service, 
            video_file, 
            video_title, 
            video_description,
            privacy_status="private" # Default to private for safety
        )
        
        # Add to playlist if configured
        playlist_id = os.getenv("YOUTUBE_PLAYLIST_ID")
        if playlist_id and uploaded_video_id:
            print(f"Adding video to playlist: {playlist_id}")
            add_video_to_playlist(youtube_service, uploaded_video_id, playlist_id)
