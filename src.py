import yt_dlp
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import os
# try:
#     os.truncate("./new_url.txt", 0)
# except FileNotFoundError:
#     pass

# extract_link_option = {'print_to_file': {'video': [('url', 'new_url.txt')]}, 'cookiefile': 'cookies.txt', 'ignoreerrors': True, 'retries': 10, 'fragment_retries': 10, 'extract_flat': 'in_playlist', 'postprocessors': [{'key': 'FFmpegConcat', 'only_multi_video': True, 'when': 'playlist'}]}
# playlist_url = "https://www.youtube.com/playlist?list=PL60DGR_RnC5yX5L_RCwJOY1V7HFQ5VsfF"
# with yt_dlp.YoutubeDL(extract_link_option) as ydl:
#     error_code = ydl.download(playlist_url)
#     sleep(10)

with (open('url.txt', 'r') as f,
      open('new_url.txt', 'r') as g):
    d1 = f.read().split()
    d2 = g.read().split()
    URLs = []
    for link in d2:
        if link not in d1:
            URLs.append(link)

ydl_opts = {'format': 'bestaudio/best', 'outtmpl': {'default': './output/%(title)s.%(ext)s'}, 'cookiefile': './cookies.txt', 'ignoreerrors': 'only_download', 'retries': 10, 'fragment_retries': 10, 'cookiefile': './cookies.txt', 'extract_flat': 'discard_in_playlist', 'final_ext': 'mp3', 'postprocessors': [{'key': 'SponsorBlock', 'categories': {'music_offtopic', 'interaction', 'selfpromo', 'sponsor', 'outro', 'intro', 'preview'}, 'api': 'https://sponsor.ajay.app', 'when': 'after_filter'}, {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '5', 'nopostoverwrites': False}, {'key': 'ModifyChapters', 'remove_chapters_patterns': [], 'remove_sponsor_segments': {'interaction', 'selfpromo', 'intro', 'outro', 'preview', 'music_offtopic', 'sponsor'}, 'remove_ranges': [], 'sponsorblock_chapter_title': '[SponsorBlock]: %(category_names)l', 'force_keyframes': False}, {'key': 'FFmpegMetadata', 'add_chapters': True, 'add_metadata': True, 'add_infojson': 'if_exists'}, {'key': 'FFmpegConcat', 'only_multi_video': True, 'when': 'playlist'}]}

downloaded = []

def download(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    if error_code: pass
    else: downloaded.append(url)
    sleep(4)

with ThreadPoolExecutor(max_workers = 20) as executor:
    futures = executor.map(download, URLs)

with open("url.txt", "w") as f:
    f.truncate()
    f.write('\n'.join(downloaded))
