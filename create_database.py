import sqlite3 as sql
from pathlib import Path
from urllib.parse import urlparse
from mutagen.id3 import ID3

conn = sql.connect("songs.sqlite")
cur = conn.cursor()
res = cur.execute("SELECT name FROM sqlite_master WHERE name='songs'")
if res.fetchone() is None:
    cur.execute("CREATE TABLE songs(id PRIMARY KEY, url, name, path)")
    conn.commit()
res = cur.execute("SELECT name FROM sqlite_master WHERE name='errors'")
if res.fetchone() is None:
    cur.execute("CREATE TABLE errors(id PRIMARY KEY, url)")


music_path = Path("./output")
for song_path in music_path.iterdir():
    if song_path.is_dir():
        continue
    song = ID3(song_path)
    song_url = song["TXXX:comment"].text[0]
    song_id = urlparse(song_url).query.split('=')[1]
    song_name = song["TIT2"].text[0]
    res = cur.execute("SELECT id FROM songs WHERE id=?", (song_id,))
    if res.fetchone() is None:
        print(f"[+] Add {song_name} with id {song_id} to database")
        cur.execute("INSERT INTO songs VALUES(?, ?, ?, ?)",
                    (song_id, song_url, song_name, song_path.name))
        conn.commit()
conn.close()
