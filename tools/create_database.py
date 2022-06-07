import sqlite3
import sys

def create_database(path:str):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('''CREATE TABLE subtitles (video_id integer, duration integer, content text, start_time integer, url text)''')
    con.commit()
    con.close()


if __name__ == '__main__':
    path = sys.argv[1]
    create_database(path)