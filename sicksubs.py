#!/usr/bin/env python
import db
import os
import sys
import time
import shlex
import sqlite3
import periscope
import subprocess

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

# if you want the subtitle file to include the language in the file name, set
# this option to True. This would result in a subtitle of the form:
#
# White.Collar.S02E04.DVDRip.XviD-SAiNTS.nl.srt
APPEND_LANG = False

#***********************************</CONFIG>*********************************


quiet = False


def sickbeard_run(conn):
    """
    This function will be called when the script is executed by sickbeard. This
    will add a final_location to the correct item in the queue, to make sure
    the subtitle file can be moved there after downloading.
    """
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
    # u'/media/bin2/usenet_downloads/tv/QI.S09E12.HDTV.XviD-FTP/qi.s09e12.
    # hdtv.xvid-ftp.avi',
    # '72716', '9', '12', '2011-11-25']
    final_loc = sys.argv[1]

    db.add_ep(conn, final_loc)
    cron_run(conn)


def cron_run(conn):
    """
    This function will be called when the script is executed by cron. This will
    read the jobs and try to find sub downloads for each of them
    """
    # get all eps
    all_eps = db.get_all_eps(conn)

    to_download = {}
    subdl = periscope.Periscope("cache")
    for ep in all_eps:
        subs = subdl.listSubtitles(ep.final_loc, [SUB_LANG])

        if subs and os.path.exists(ep.final_loc):
            to_download[ep] = subs
        else:
            ep_name = os.path.splitext(os.path.expanduser(ep.final_loc))[0]
            if os.path.exists(ep_name + '.srt'):
                # Mabe user downloaded sub for this ep manually?
                db.remove_single(conn, ep)
                print(u'Cleaned up db because ' + ep_name + ' already has subs!')
            elif not os.path.exists(ep.final_loc):
                db.remove_single(conn, ep)
                print(u'Cleaned up db because ' + ep_name + ' is no longer available on disk!')
            time.sleep(3)

    if not to_download:
        if not quiet:
            print "No subs available for any of your eps yet!"
        return True
    successful = []
    for d in to_download:
        if subdl.attemptDownloadSubtitle(to_download[d], [SUB_LANG]) is not None:
            successful.append(d)

    # remove successfully downloaded files from db
    db.remove_downloaded(conn, successful)
    # call post-processing for successfully downloaded files
    if POST_CALL:
        for d in successful:
            for script in POST_CALL.split(','):
                to_call = shlex.split(script)
                to_call.append(d.final_loc)
                subprocess.call(to_call)


if __name__ == '__main__':
    if '-q' in sys.argv:
        quiet = True
        sys.argv.remove('-q')

    if not os.path.exists(DATABASE_FILE):
        conn = db.initialize(DATABASE_FILE)
    else:
        conn = sqlite3.connect(DATABASE_FILE)

    if len(sys.argv) == 7 or len(sys.argv) == 2:
        sickbeard_run(conn)
    else:
        cron_run(conn)
