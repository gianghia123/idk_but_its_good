import yt_dlp
from concurrent.futures import ThreadPoolExecutor
from time import sleep

with open('file.txt', 'r') as links:
    URLs = links.read().splitlines()

ydl_opts = {'format': 'bestaudio/best', 'outtmpl': {'default': './output/%(title)s.%(ext)s'}, 'ignoreerrors': 'only_download', 'retries': 10, 'fragment_retries': 10, 'cookiefile': './cookies.txt', 'extract_flat': 'discard_in_playlist', 'final_ext': 'mp3', 'postprocessors': [{'key': 'SponsorBlock', 'categories': {'music_offtopic', 'interaction', 'selfpromo', 'sponsor', 'outro', 'intro', 'preview'}, 'api': 'https://sponsor.ajay.app', 'when': 'after_filter'}, {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '5', 'nopostoverwrites': False}, {'key': 'ModifyChapters', 'remove_chapters_patterns': [], 'remove_sponsor_segments': {'interaction', 'selfpromo', 'intro', 'outro', 'preview', 'music_offtopic', 'sponsor'}, 'remove_ranges': [], 'sponsorblock_chapter_title': '[SponsorBlock]: %(category_names)l', 'force_keyframes': False}, {'key': 'FFmpegMetadata', 'add_chapters': True, 'add_metadata': True, 'add_infojson': 'if_exists'}, {'key': 'FFmpegConcat', 'only_multi_video': True, 'when': 'playlist'}]}

downloaded = []

def download(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    if error_code: pass
    else: downloaded.append(url)
    sleep(1)

with ThreadPoolExecutor(max_workers = 20) as executor:
    futures = executor.map(download, URLs)

with open("output/downloaded", "w") as f:
    f.write('\n'.join(downloaded))
