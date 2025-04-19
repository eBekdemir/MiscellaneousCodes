import os
from pathlib import Path
import sys

documents_path = str(Path.home() / "Music")

def download_mp3(url):
    os.system(f'yt-dlp -x --audio-format mp3 -P "{documents_path}" "{url}"')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        link = sys.argv[1]
    else:
        link = input("Enter YouTube URL: ")
    download_mp3(link)
