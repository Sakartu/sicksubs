#!/usr/bin/python
from rss.RSS import TrackingChannel
import sqlite3
import os
from operator import itemgetter

DB = u'~/.local/share/next/next.db'

def main():
    c = TrackingChannel()
    c.parse(u'http://feeds.bierdopje.com/bierdopje/subs/english')
    shownames = get_shownames()
    for k in c.keys():
        subname = str(k)[str(k).rfind('/') + 1:]
        for showname in shownames:
            if set(showname.lower().split(' ')) <= set(subname.lower().split('.')):
                pass

                # found a show that matches


def get_shownames():
    conn = sqlite3.connect(os.path.expandvars(os.path.expanduser(DB)))
    shownames = []
    with conn:
        c = conn.cursor()
        shownames = c.execute(u'''SELECT name FROM shows''').fetchall()
    return map(itemgetter(0), shownames)



if __name__ == '__main__':
    main()
