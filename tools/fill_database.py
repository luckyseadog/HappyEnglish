import sqlite3
import sys
from typing import List
from urllib.error import HTTPError
from urllib.request import urlopen
import json
import tqdm
import re
import time


def download_subs(video_id: int) -> List[dict]:
    response = urlopen(f'https://www.ted.com/talks/subtitles/id/{video_id}/lang/en')
    data = response.read().decode('utf-8')
    captions = json.loads(data)['captions']

    response_site = urlopen(f'https://www.ted.com/talks/{video_id}')
    data_site = response_site.read().decode('utf-8')

    for caption in captions:
        caption['url'] = re.findall(r'https://hls\.ted\.com/project_masters/\d+/manifest\.m3u8\?intro_master_id=2346', data_site)[0]

    return [(video_id, caption['duration'], caption['content'], caption['startTime'], caption['url']) for caption in captions]


def fill_database(captions, path):
    con = sqlite3.connect(path)
    con.execute('DELETE FROM subtitles ;')
    cur = con.cursor()
    cur.executemany('''INSERT INTO subtitles VALUES (?, ?, ?, ?, ?)''', captions)
    con.commit()
    con.close()


if __name__ == '__main__':
    path = sys.argv[1]
    captions = []

    for i in tqdm.tqdm(range(1, 100)):
        try:
            time.sleep(1)
            captions += download_subs(i)
        except HTTPError:
            continue
    fill_database(captions, path)
