import os
import re
import asyncio
import yt_dlp
import aiohttp

from youtubesearchpython.__future__ import VideosSearch

# ------------------------------
#  CONFIG
# ------------------------------
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "40385376567b497f9dda4a2482c57187")  # apna API key yaha dalna hai

# ------------------------------
#  SEARCH FUNCTION
# ------------------------------
async def yt_search(query: str):
    """
    YouTube par query search karke ek result deta hai.
    """
    try:
        search = VideosSearch(query, limit=1)
        results = await search.next()
        if not results["result"]:
            return None

        data = results["result"][0]
        return {
            "title": data["title"],
            "duration": data.get("duration"),
            "views": data.get("viewCount", {}).get("short"),
            "channel": data["channel"]["name"],
            "link": data["link"],
            "id": data["id"],
            "thumbnails": data["thumbnails"][0]["url"] if data.get("thumbnails") else None,
        }
    except Exception as e:
        print(f"yt_search error: {e}")
        return None


# ------------------------------
#  DOWNLOAD FUNCTION
# ------------------------------
async def yt_download(url: str, audio: bool = True):
    """
    YouTube se audio/video download karta hai.
    """
    try:
        ydl_opts = {
            "format": "bestaudio/best" if audio else "best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "ext": info.get("ext"),
                "filepath": ydl.prepare_filename(info),
            }
    except Exception as e:
        print(f"yt_download error: {e}")
        return None


# ------------------------------
#  DIRECT STREAM LINK
# ------------------------------
async def yt_stream(url: str, audio: bool = True):
    """
    YouTube se direct stream link (without download) deta hai.
    """
    try:
        ydl_opts = {
            "format": "bestaudio/best" if audio else "best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
            return {
                "title": info.get("title"),
                "url": info["url"],
                "duration": info.get("duration"),
                "id": info.get("id"),
            }
    except Exception as e:
        print(f"yt_stream error: {e}")
        return None


# ------------------------------
#  TEST (sirf check karne ke liye)
# ------------------------------
if __name__ == "__main__":
    async def main():
        query = "Alan Walker Faded"
        result = await yt_search(query)
        print("Search Result:", result)

        if result:
            stream = await yt_stream(result["link"])
            print("Stream Info:", stream)

    asyncio.run(main())
