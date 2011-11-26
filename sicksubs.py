#!/usr/bin/python
import db
import os
import sys
import sqlite3
import urllib2
import bierdopje
import nameparser

#***********************************<CONFIG>************************************
# These are parameters that you may want to configure, although the defaults are
# quite sane 

# location where sicksubs should store the queue file
DATABASE_FILE = u'~/.sicksubs/sicksubs.db' 

# the language of the downloaded subs, can be nl or en
SUB_LANG = 'en'

#***********************************</CONFIG>***********************************

def sickbeard_run(conn):
    '''
    This function will be called when the script is executed by sickbeard. This
    will add a final_location to the correct item in the queue, to make sure the
    subtitle file can be moved there after downloading.
    '''
    # It passes 5 parameters to these scripts: 
    # 1 final full path to the episode file
    # 2 original name of the episode file
    # 3 show tvdb id
    # 4 season number
    # 5 episode number
    # 6 episode air date
    # example call:
    # ['/home/sickbeard/sicksubs/sicksubs.py', 
    # u'/media/media/Series/Qi/Season 09/QI.S09E12.Illumination.avi', 
    # u'/media/bin2/usenet_downloads/tv/QI.S09E12.HDTV.XviD-FTP/qi.s09e12.hdtv.xvid-ftp.avi', 
    # '72716', '9', '12', '2011-11-25']
    final_loc = sys.argv[1]
    interm_loc = sys.argv[2]
    tvdbid = sys.argv[3]

    db.add_ep(conn, interm_loc, final_loc, tvdbid)

def cron_run(conn):
    '''
    This function will be called when the script is executed by cron. This will
    read the jobs and try to find sub downloads for each of them
    '''
    # get all eps
    all_eps = db.get_all_eps(conn)
    
    to_download = []
    for ep in all_eps:
        if ep.sid and ep.season and ep.ep:
            sublinks = bierdopje.get_subs(ep.sid, SUB_LANG, ep.season, ep.ep)
            sub = nameparser.find_link(ep.job_name, sublinks)
            if sub:
                ep.sub = sub
                to_download.append(ep)

    download(to_download)
    db.remove_downloaded(conn, to_download)

def download(to_download):
    '''
    This helper method downloads a sub to a filed named as the episode, but with
    a subtitle extension
    '''
    for ep in to_download:
        baseloc = os.path.splitext(os.path.expanduser(ep.final_loc))[0]
        resp = urllib2.urlopen(ep.sub)

        if 'content-disposition' in resp.info().dict:
            subext = os.path.splitext(resp.info().dict['content-disposition'])[1]
        else:
            subext = '.srt'
        content = resp.read()
        with open(os.path.join(baseloc + subext), 'w+') as sub:
            sub.write(content)

def update_tvdbids(sids, tvdbid):
    if tvdbid not in sids:
        sid = bierdopje.get_show_id(tvdbid)
        sids[tvdbid] = sid
    return sids

if __name__ == '__main__':
    if len(sys.argv) == 2:
        db_path = sys.argv[2]
    else:
        db_path = DATABASE_FILE
 
    if not os.path.exists(db_path):
        conn = db.initialize(db_path)
    else:
        conn = sqlite3.connect(db_path)

    if len(sys.argv) == 7:
        sickbeard_run(conn)
    else:
        cron_run(conn)
