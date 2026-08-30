from . import download
from . import dvd
from . import app
from . import scrapChannel
from . import createImages
from pathlib import Path
# import download
# import dvd
# import app
# import scrapChannel
# import createImages
import shutil



def move(basePath, inFiles):
    for key, file in inFiles.items():
        if (file) and ("." in key):
            shutil.move(file, str(basePath/ 'background' / key))

def main():
    myInput, ytName, background = app.getInput()
    
    if background['ImageMode'] == 'youtube':
        _, _, ytName = background['YouTubeChannel'].partition("@")

    basePath = Path(__file__).resolve().parent.parent.parent / "Youtubers" / ytName
    print(ytName)

    dl = download.Download(basePath, myInput)
    dl.writeVidInfo()
    numVideos, totDur = dl.downloadVideos()
    videoData = dl.getVideoData()

    if background['ImageMode'] == 'local':
        move(basePath, background)
    elif background['ImageMode'] == 'youtube':
        bannerPath, pfpPath, title, username, description = scrapChannel.getChannelInfo(basePath, background['YouTubeChannel'])
        images = createImages.CreateImages(basePath, bannerPath, title, username, description, numVideos, totDur//60)
        images.createBackground()
        images.createChapterBackground()

    # for video in videoData:
    #     print(video)
    myDvd = dvd.DVD(videoData, ytName)

    with (basePath / (ytName+".dvds")).open("w", encoding="utf-8") as f:
        f.write(myDvd.styler())
    app.finish()

if __name__ == "__main__":
    main()