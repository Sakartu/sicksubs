#!/usr/bin/python
import db
import os
import sys
import pickle
import sqlite3
import urllib2
import bierdopje
import nameparser

#***********************************<CONFIG>************************************
# These are parameters that you may want to configure, although the defaults are
# quite sane 

# location where sabsub should store the queue file
DATABASE_FILE = u'~/.sabsub/sabsub.db' 

# the language of the downloaded subs, can be nl or en
SUB_LANG = 'en'

#***********************************</CONFIG>***********************************


def sabnzbd_run(conn):
    '''
    This function will be called when the script is executed by sabnzbd+. This
    will add a show job to the queue, so that it can be downloaded from
    bierdopje.
    '''
    # parameters for the script are:
    # 1   The final directory of the job (full path)
    # 2   The original name of the NZB file
    # 3   Clean version of the job name (no path info and ".nzb" removed)
    # 4   Indexer's report number (if supported)
    # 5   User-defined category
    # 6   Group that the NZB was posted in e.g. alt.binaries.x
    # 7   Status of post processing. 0 = OK, 1=failed verification, 2=failed unpack, 3=1+21
    if sys.argv[7] != '0':
        print('Post-processing failed, ignoring subtitle download')
        return -1

    interm_loc = sys.argv[1]
    job_name = sys.argv[3]
    db.add_ep(conn, job_name, interm_loc)

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
    final_loc = sys.argv[1]
    interm_loc = sys.argv[2]
    tvdbid = sys.argv[3]

    db.update_ep(conn, interm_loc, final_loc, tvdbid)

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

def read_queue():
    '''
    This helper function opens the queue file and checks whether the type is
    correct
    '''
    with open(DATABASE_FILE, 'rb') as f:
        jobs = pickle.load(f)

    if type(jobs) != type(set()):
        jobs = set()

    return jobs

def write_queue(jobs):
    '''
    This helper function opens the queue file and writes a new job queue to it
    '''
    with open(DATABASE_FILE, 'w+') as f:
        pickle.dump(jobs, f)

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

    if len(sys.argv) == 8:
        sabnzbd_run(conn)
    elif len(sys.argv) == 7:
        sickbeard_run(conn)
    else:
        cron_run(conn)

