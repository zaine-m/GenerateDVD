from yt_dlp import YoutubeDL
from pathlib import Path
from . import shorten
# import shorten

def timestampSort(e):
    return e['timestamp'] if e['timestamp'] is not None else float('inf')

def formatTime(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

class Download:
    def __init__(self, basePath, myInput='Download.txt', REMOVE_OVERFLOW=True, AUTO_SHORTEN_TITLES=True):
        self.basePath = basePath
        self.fileNamesDict = {
            'default': str(self.basePath / "Videos" / "%(title).20s.%(ext)s"),
            'subtitle': str(self.basePath / "Subtitles" / "%(title).20s.%(ext)s"),
            'thumbnail': str(self.basePath / "Thumbnails" / "%(title).20s.%(ext)s")
        }

        self.urls = self.getUrls(myInput)
        self.videoData = self.getVideoInfo()
        if REMOVE_OVERFLOW:
            self.videoData = self.capLength()
        if AUTO_SHORTEN_TITLES:
            self.videoData = shorten.shortenTitles(self.videoData)

    def getVideoData(self):
        return self.videoData

    def downloadSubs(self):
        YTDL_PARAMETERS = {
            'http_timeout': 60,
            'writesubtitles': True, 
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-GB', 'en-US'],
            'write-subs': True, 
            'subtitlesformat': 'srt',
            'writethumbnail': True,
            'format': 'bv*[height<=480]+ba/b[height<=480]',
            'no-overwrites': True,
            'nooverwrites': True,
            'continue': True,
            'outtmpl':self.fileNamesDict,
            'restrictfilenames': True,
            'sponsorblock-remove': 'sponsor',
            'postprocessors': [{
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
            }]
        }
        urls = [video["url"] for video in self.videoData]
        with YoutubeDL(YTDL_PARAMETERS) as ydl:
            ydl.download(urls)
    
    def downloadVideos(self):
        YTDL_PARAMETERS = {
            'js_runtimes': {
                'deno': {}
            },
            'http_timeout': 60,
            'writesubtitles': True, 
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-GB', 'en-US'],
            'write-subs': True, 
            'subtitlesformat': 'srt',
            'writethumbnail': True,
            'format': 'mp4',
            'no-overwrites': True,
            'nooverwrites': True,
            'continue': True,
            'outtmpl':self.fileNamesDict,
            'restrictfilenames': True,
            'sponsorblock-remove': 'sponsor',
            'postprocessors': [{
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
            }]
        }
        urls = []
        totalDuration = 0
        for video in self.videoData:
            urls.append(video["url"])
            totalDuration += video["duration"]

        with YoutubeDL(YTDL_PARAMETERS) as ydl:
            ydl.download(urls)
        return len(urls), totalDuration

    def writeVidInfo(self):
        path = self.basePath / "Chapters.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8")  as file:
            file.write("---RELEASE-DATE---|-DURATION-|------FILENAME------|-----------------------------------TITLE-----------------------------------|---------------------URL---------------------|--------------CHAPTERS--------------\n")
            for video in self.videoData:
                file.write("|".join([str(video['timestamp']).ljust(18)[:18], str(video['duration']).ljust(10)[:10], str(video['title']).ljust(20)[:20], str(video['full title']).ljust(75)[:75], str(video['url']).ljust(45)[:45], str(video['chapters'])]))
                file.write("\n")

    def capLength(self, limit=13200):
        dp = [None] * (limit + 1)
        dp[0] = []
        for i, video in enumerate(self.videoData):
            duration = video["duration"]
            for total in range(limit, duration - 1, -1):
                if dp[total - duration] is not None:
                    candidate = dp[total - duration] + [i]
                    if dp[total] is None:
                        dp[total] = candidate
        best = max(
            (combo for combo in dp if combo is not None),
            key=lambda combo: sum(self.videoData[i]["duration"] for i in combo)
        )
        removed = [video for i, video in enumerate(self.videoData) if i not in best]
        for video in removed:
            print(f"Removed: {video['title']}")
        return [self.videoData[i] for i in best]

    def getUrls(self, myInput):
        """string(text file of urls or playlist link) -> array of strings(urls)"""
        if ".txt" in myInput:
            with open('Download.txt', 'r') as file:
                urls = [line.strip() for line in file]
        elif "youtube.com/playlist" in myInput:
            with YoutubeDL({'extract_flat':True, 'skip_download':True}) as ydl:
                info = ydl.extract_info(myInput, download=False)
            urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in info["entries"]]
        return urls

    def getVideoInfo(self):
        totalDuration = 0
        videos = [] 
        with YoutubeDL({'skip_download': True, 'outtmpl': self.fileNamesDict, 'restrictfilenames': True}) as ydl:
            for url in self.urls:
                info = ydl.extract_info(url, download=False)

                video = {} # duration, title, chapters, timestamp
                video['timestamp'] = (info.get('timestamp'))
                video['title'] = Path(ydl.prepare_filename(info)).stem
                video['duration'] = info.get('duration')
                video['full title'] = info.get('title')
                video['url'] = url
                totalDuration += info.get('duration')

                # print("TITLE:", video['title'])
                # print("TIMESTAMP:", video['timestamp'])
                # print("DURATION:", video['duration'])

                chapters = info.get('chapters')
                chaps = []
                if chapters:
                    for chapter in chapters:
                        chaps.append(formatTime(chapter['start_time']))
                # else:
                    # print("NO CHAPTERS")
                video['chapters'] = chaps
                videos.append(video)
        videos.sort(key=timestampSort, reverse=True)
        return videos