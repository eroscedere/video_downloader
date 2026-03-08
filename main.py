from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp
import os
import uuid
import threading

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

progress_dict = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/info")
def get_video_info(url: str):

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "url": url
    }


@app.get("/progress")
def get_progress(download_id: str):
    return {"progress": progress_dict.get(download_id, 0)}


@app.get("/download")
def download_video(url: str):

    download_id = str(uuid.uuid4())
    filepath = f"{DOWNLOAD_FOLDER}/{download_id}.mp4"

    progress_dict[download_id] = 0

    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)

            if total:
                percent = int(downloaded / total * 100)
                progress_dict[download_id] = percent

        if d["status"] == "finished":
            progress_dict[download_id] = 100

    def run_download():

        ydl_opts = {
            "format": "best",
            "outtmpl": filepath,
            "progress_hooks": [hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    threading.Thread(target=run_download).start()

    return {"download_id": download_id, "file": f"/file/{download_id}"}


@app.get("/file/{download_id}")
def get_file(download_id: str):

    filepath = f"{DOWNLOAD_FOLDER}/{download_id}.mp4"

    return FileResponse(
        filepath,
        filename="video.mp4",
        media_type="application/octet-stream"
    )
