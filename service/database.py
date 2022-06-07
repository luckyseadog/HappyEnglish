from dataclasses import dataclass
from typing import List
import sqlite3


@dataclass
class VideoFragment:
    video_id: int
    duration: int
    content: str
    startTime: int
    url: str

def search(phrase:tuple, path:str) -> List[VideoFragment]:
    con = sqlite3.connect(path)
    cur = con.cursor()
    raws = cur.execute('''SELECT * FROM subtitles WHERE content LIKE ?''', [f'%{phrase}%'])
    con.commit()
    result = []
    for raw in raws:
        result.append(VideoFragment(*raw))
    con.close()
    return result

