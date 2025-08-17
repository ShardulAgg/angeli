from upload_post import UploadPostClient

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("UPLOAD_POST_API_KEY")
client = UploadPostClient(api_key=api_key)


async def push_content(video_path:str, title:str):
    response = client.upload_video(
    video_path=video_path,
    title=title,
    user="angeli",
    platforms=["instagram"]
    )

    return response