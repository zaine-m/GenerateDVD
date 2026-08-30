import os
import requests
import yt_dlp
from io import BytesIO
from PIL import Image

def getChannelInfo(basePath, channelLink):
    # output_dir = str(basePath / 'channel_info')
    output_dir = str(basePath) + '\\HomePage'
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "skip_download": True,
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
        "playlist_items": "0",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channelLink, download=False)

    title = (info.get("channel") or info.get("uploader") or info.get("title"))
    username = (info.get("id") or info.get("uploader_id"))
    description = (info.get("description") or "")
    thumbnails = info.get("thumbnails") or []

    avatarUrls = []
    bannerUrls = []

    for thumbnail in thumbnails:
        if not isinstance(thumbnail, dict):
            continue
        elif ('banner' in thumbnail["id"]) and not('uncropped' in thumbnail["id"]):
            bannerUrls.append(thumbnail['url'])
        elif thumbnail["id"] in "0, 1, 2, 3, 4, 5":
            bannerUrls.append(thumbnail['url'])
        elif ('avatar' in thumbnail['id'])and not('uncropped' in thumbnail["id"]):
            avatarUrls.append(thumbnail['url'])
        elif thumbnail['id']=='7':
            avatarUrls.append(thumbnail['url'])

    def download_image(urls, filename):
        if not urls:
            return None

        path = os.path.join(output_dir, filename)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0 Safari/537.36"
            ),
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.youtube.com/",
        }

        best_image = None
        best_size = 0

        for url in urls:
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=20,
                )
                response.raise_for_status()

                content_type = response.headers.get("Content-Type", "").lower()

                if not content_type.startswith("image/"):
                    continue

                # Check the actual image dimensions
                image = Image.open(BytesIO(response.content))
                width, height = image.size
                size = width * height

                # Keep the highest-resolution image
                if size > best_size:
                    best_size = size
                    best_image = response.content

            except (requests.RequestException, OSError):
                continue

        if best_image is None:
            return None

        try:
            with open(path, "wb") as f:
                f.write(best_image)

            return path

        except OSError:
            return None

    pfpPath = download_image(avatarUrls,output_dir+"\\ChannelPic.jpg")
    bannerPath = download_image(bannerUrls,output_dir+"\\Banner.jpg")

    return bannerPath, pfpPath, title, username, description

# print(getChannelInfo("C:\\Users\\Lenovo\\Downloads", "https://www.youtube.com/@pumpykinq"))