#!/usr/bin/python
from rss.RSS import TrackingChannel
import os
import sys
import pickle
import urllib2

FEED = u'http://feeds.bierdopje.com/bierdopje/subs/english'
QUEUE_FILE = u'/tmp/sabsub_queue'
API_KEY = u'6935AC4D8CF45C7A'

class Queueitem(object):
    def __init__(self, job_name, interm_loc):
        self.job_name = job_name
        self.interm_loc = interm_loc
        self.final_loc = None

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
    jobs.append(Queueitem(job_name, interm_loc))
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

    jobs = read_queue()
    for job in jobs:
        if isinstance(job, Queueitem) and job.interm_loc == interm_loc:
            job.final_loc = final_loc
    write_queue(jobs)

def cron_run():
    '''
    This function will be called when the script is executed by cron. This will
    read the jobs and try to find sub downloads for each of them
    '''
    jobs = read_queue()

    c = TrackingChannel()
    c.parse(FEED)
    for k in c.keys():
        subname = str(k)[str(k).rfind('/') + 1:]
        with open(QUEUE_FILE) as f:
            jobs = pickle.load(f)
            for (name, loc) in jobs.items():
                if name in subname:
                    import pprint
                    pprint.pprint(dict(c)[k])
                    #download(k, loc)
def read_queue():
    '''
    This helper function opens the queue file and checks whether the type is
    correct
    '''
    with open(QUEUE_FILE, 'rb') as f:
        jobs = pickle.load(f)

    if type(jobs) != type([]):
        jobs = []

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
    subext = os.path.splitext(url)[1]
    baseloc = os.path.splitext(loc)[0]
    with open(baseloc + subext, 'w+') as sub:
        resp = urllib2.urlopen(url)
        sub.write(resp.read())

if __name__ == '__main__':
    if len(sys.argv) == 8:
        sabnzbd_run()
    elif len(sys.argv) == 7:
        sickbeard_run()
    else:
        cron_run()

