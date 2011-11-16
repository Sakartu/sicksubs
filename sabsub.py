#!/usr/bin/python
import os
import sys
import pickle
import urllib2
import bierdopje
import nameparser

#***********************************<CONFIG>************************************
# These are parameters that you may want to configure, although the defaults are
# quite sane 

# location where sabsub should store the queue file
QUEUE_FILE = u'/tmp/sabsub_queue' 

# the language of the downloaded subs, can be nl or en
SUB_LANG = 'en'

#***********************************</CONFIG>***********************************


class Queueitem(object):
    def __init__(self, job_name, interm_loc, final_loc=None, tvdbid=None):
        self.job_name = job_name
        self.interm_loc = interm_loc
        self.final_loc = final_loc
        self.tvdbid = tvdbid
 
    def __repr__(self):
        return str(self.tvdbid) + ":" + str(self.job_name)

def sabnzbd_run():
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

    jobs = read_queue()
    jobs.add(Queueitem(job_name, interm_loc))
    write_queue(jobs)

def sickbeard_run():
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

    jobs = read_queue()
    for job in jobs:
        if isinstance(job, Queueitem) and job.interm_loc == interm_loc:
            job.final_loc = final_loc
            job.tvdbid = tvdbid
            write_queue(jobs)
            return

def cron_run(jobs=None):
    '''
    This function will be called when the script is executed by cron. This will
    read the jobs and try to find sub downloads for each of them
    '''
    if not jobs:
        jobs = read_queue()

    to_download = set()
    for job in jobs:
        sid = bierdopje.get_show_id(job.tvdbid)
        (season, ep) = nameparser.get_ep_details(job.job_name)
        if sid and season and ep:
            sublinks = bierdopje.get_subs(sid, SUB_LANG, season, ep)
            job.sub = nameparser.find_link(job, sublinks)
            if job.sub:
                to_download.add(job)

    for job in to_download:
        download(job.sub, job.final_loc)
    write_queue(set(jobs) - to_download)

def read_queue():
    '''
    This helper function opens the queue file and checks whether the type is
    correct
    '''
    with open(QUEUE_FILE, 'rb') as f:
        jobs = pickle.load(f)

    if type(jobs) != type(set()):
        jobs = set()

    return jobs

def write_queue(jobs):
    '''
    This helper function opens the queue file and writes a new job queue to it
    '''
    with open(QUEUE_FILE, 'w+') as f:
        pickle.dump(jobs, f)

def download(url, loc):
    '''
    This helper method downloads a sub to a filed named as the episode, but with
    a subtitle extension
    '''
    baseloc = os.path.splitext(os.path.expanduser(loc))[0]
    resp = urllib2.urlopen(url)

    if 'content-disposition' in resp.info().dict:
        subext = os.path.splitext(resp.info().dict['content-disposition'])[1]
    else:
        subext = '.srt'
    with open(baseloc + subext, 'w+') as sub:
        sub.write(resp.read())

if __name__ == '__main__':
    if len(sys.argv) == 8:
        sabnzbd_run()
    elif len(sys.argv) == 7:
        sickbeard_run()
    else:
        t = Queueitem('Terra.Nova.S01E06.HDTV.XviD-LOL', 'bla', '/media/media/Series/Terra Nova/Season 01/Terra.Nova.S01E06.Nightfall.avi', tvdbid='164091')
        #t = Queueitem('Terra Nova', 'bla', 'bla')
        cron_run([t])

