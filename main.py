from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import yt_dlp
import json

class YT_Video(BaseModel):
    url: str | None = "https://www.youtube.com/watch?v=BaW_jenozKc"

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/testYtDlp")
def read_root():
    URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']
    with yt_dlp.YoutubeDL() as ydl:
        ydl.download(URLS)

@app.get("/testAudio")
def read_root():
    URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)

@app.post("/testInfo")
async def create_item(yt_video: YT_Video):
    URL = yt_video.url

    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        # return json.dumps(ydl.sanitize_info(info))
        return info
    
@app.get("/testLogger")
def read_root():
    URLS = ['https://www.youtube.com/watch?v=BaW_jenozK']

    class MyLogger:
        def debug(self, msg):
            # For compatibility with youtube-dl, both debug and info are passed into debug
            # You can distinguish them by the prefix '[debug] '
            if msg.startswith('[debug] '):
                pass
            else:
                self.info(msg)

        def info(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            return msg


    # ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now post-processing ...')


    ydl_opts = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)