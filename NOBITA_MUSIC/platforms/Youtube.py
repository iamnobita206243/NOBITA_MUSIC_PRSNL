from config import BABYAPI


async def download_song(link: str):
    from Spy import app
    x = re.compile(
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([A-Za-z0-9_-]{11})'
    )
    video_id = x.search(link)
    vidid = video_id.group(1) if video_id else link

    xyz = os.path.join("downloads", f"{vidid}.mp3")
    if os.path.exists(xyz):
        return xyz

    loop = asyncio.get_running_loop()

    def get_url():
        api_url = f"{BABYAPI}/song?query={vidid}"
        try:
            return requests.get(api_url).json().get("link")
        except:
            return None

    download_url = await loop.run_in_executor(None, get_url)
    parsed = urlparse(download_url)
    parts = parsed.path.strip("/").split("/")
    cname, msgid = str(parts[0]), int(parts[1])
    msg = await app.get_messages(cname, msgid)
    await msg.download(file_name=xyz)

    while not os.path.exists(xyz):
        await asyncio.sleep(0.5)

    return xyz
