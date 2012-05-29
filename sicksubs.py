#!/usr/bin/env python
import db
import os
import sys
import shlex
import sqlite3
import urllib2
import bierdopje
import subprocess
import nameparser

#***********************************<CONFIG>***********************************
# These are parameters that you may want to configure, although the defaults
# are quite sane

# location where sicksubs should store the queue file
DATABASE_FILE = u'~/.sicksubs/sicksubs.db'

# the language of the downloaded subs, can be nl or en
SUB_LANG = 'en'

# post-processing script(s), will be called with one argument on successful
# sub download, the name of the ep for which a sub was found
#
# multiple scripts can be separated by comma's. do _not_ use unicode strings
# since the shlex module does not support unicode prior to 2.7.3
POST_CALL = ''  # '/home/peter/test.sh,/home/peter/test2.sh'
#POST_CALL = './test.sh'

#***********************************</CONFIG>*********************************


def sickbeard_run(conn):
    '''
    This function will be called when the script is executed by sickbeard. This
    will add a final_location to the correct item in the queue, to make sure the
    subtitle file can be moved there after downloading.
    '''
    # It passes 6 parameters to these scripts:
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
    cron_run(conn)


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
            if sub and os.path.exists(ep.final_loc):
                ep.sub = sub
                to_download.append(ep)
            else:
                ep_name = os.path.splitext(os.path.expanduser(ep.final_loc))[0]
                if os.path.exists(ep_name + '.srt'):
                    # Mabe user downloaded sub for this ep manually?
                    db.remove_single(conn, ep)
                    print u'Cleaned up db because ' + ep_name + ' already has subs!'
                elif not os.path.exists(ep.final_loc):
                    db.remove_single(conn, ep)
                    print u'Cleaned up db because ' + ep_name + ' is no longer available on disk!'

    if not to_download:
        print "No subs available for any of your eps yet!"
        return True
    for d in to_download:
        d.result = download(d)
    # remove successfully downloaded files from db
    successful = filter(lambda x : x.result, to_download)
    db.remove_downloaded(conn, successful)
    # check if all files are parsed successfully
    result = all([ep.result for ep in to_download])
    # call post-processing for successfully downloaded files
    if not POST_CALL:
        return result

    for d in successful:
        for script in POST_CALL.split(','):
            to_call = shlex.split(script)
            to_call.append(d.final_loc)
            subprocess.call(to_call)
    # return result
    return result

def download(ep):
    '''
    This helper method downloads a sub to a file named as the episode, but with
    a subtitle extension
    '''
    try:
        ep_loc = os.path.expanduser(ep.final_loc)
        ep_stat = os.stat(ep_loc)
        ep_perms = ep_stat.st_mode
        ep_uid = ep_stat.st_uid
        ep_gid = ep_stat.st_gid
        baseloc = os.path.splitext(ep_loc)[0]
        resp = urllib2.urlopen(ep.sub)

        if 'content-disposition' in resp.info().dict:
            subext = os.path.splitext(resp.info().dict['content-disposition'])[1]
        else:
            subext = '.srt'
        content = resp.read()
        sub_path = os.path.join(baseloc + subext)
        with open(sub_path, 'w+') as sub:
            sub.write(content)
            os.chown(sub_path, ep_uid, ep_gid)
            os.chmod(sub_path, ep_perms)
            print "Successfully downloaded subs for {0}".format(baseloc)
    except Exception, e:
        print "Couldn't download sub for ep {name}:".format(name=ep.final_loc)
        print e
        return False
    return True

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
