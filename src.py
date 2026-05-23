import yt_dlp
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import os
import sqlite3 as sql
from urllib.parse import urlparse

try:
    os.truncate("./new_url.txt", 0)
except FileNotFoundError:
    pass
conn = sql.connect("songs.sqlite")
cur = conn.cursor()

extract_link_option = {'print_to_file': {'video': [('url', 'new_url.txt')]}, 'cookiefile': 'cookies.txt', 'ignoreerrors': True, 'retries': 10,
                       'fragment_retries': 10, 'extract_flat': 'in_playlist', 'postprocessors': [{'key': 'FFmpegConcat', 'only_multi_video': True, 'when': 'playlist'}]}
playlist_url = "https://www.youtube.com/playlist?list=PL60DGR_RnC5yX5L_RCwJOY1V7HFQ5VsfF"
with yt_dlp.YoutubeDL(extract_link_option) as ydl:
    error_code = ydl.download(playlist_url)
    print("[+] Sleep a bit...")
    sleep(300)

with open('new_url.txt', 'r') as g:
    d = g.read().split()
    URLs = []
    for link in d:
        res = cur.execute("SELECT url FROM songs WHERE url=?", (link,))
        if res.fetchone() is None:
            URLs.append(link)
        else:
            pass

print(len(URLs))
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': {
        'default': './output/%(title)s.%(ext)s',
        'pl_thumbnail': ''
    },
    'ignoreerrors': 'only_download',
    'retries': 10,
    'fragment_retries': 10,
    'cookiefile': './cookies.txt',
    'extract_flat': 'discard_in_playlist',
    'final_ext': 'wav',
    'postprocessors': [
        {
            'key': 'SponsorBlock',
            'categories': {
                'music_offtopic', 'hook', 'preview',
                'interaction', 'filler', 'sponsor',
                'outro', 'intro', 'selfpromo'
            },
            'api': 'https://sponsor.ajay.app',
            'when': 'after_filter'
        },
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '3--embed-thumbnail',
            'nopostoverwrites': False
        },
        {
            'key': 'ModifyChapters',
            'remove_chapters_patterns': [],
            'remove_sponsor_segments': {
                'music_offtopic', 'hook', 'preview',
                'interaction', 'filler', 'sponsor',
                'outro', 'intro', 'selfpromo'
            },
            'remove_ranges': [],
            'sponsorblock_chapter_title': '[SponsorBlock]: %(category_names)l',
            'force_keyframes': False
        },
        {
            'key': 'FFmpegMetadata',
            'add_chapters': True,
            'add_metadata': True,
            'add_infojson': 'if_exists'
        },
        {
            'key': 'FFmpegConcat',
            'only_multi_video': True,
            'when': 'playlist'
        }
    ]
}
downloaded = []


def download(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
    if error_code is None:
        downloaded.append(url)
    print("[+] Sleep...")
    sleep(60)


with ThreadPoolExecutor(max_workers=20) as executor:
    futures = executor.map(download, URLs)

conn.close()
