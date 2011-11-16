#!/usr/bin/python
from rss.RSS import TrackingChannel
import os
import sys
import pickle
import urllib2

FEED = u'http://feeds.bierdopje.com/bierdopje/subs/english'
QUEUE_FILE = u'/tmp/sabsub_queue'


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

    final_loc = sys.argv[1]
    job_name = sys.argv[3]
    with open(QUEUE_FILE, 'rb') as f:
        jobs = pickle.load(f)

    if type(jobs) != type({}):
        jobs = {}

    jobs[job_name] = final_loc
    with open(QUEUE_FILE, 'w+') as f:
        pickle.dump(jobs, f)

def cron_run():
    '''
    This function will be called when the script is executed by cron. This will
    read the jobs and try to find sub downloads for all of them
    '''
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
        # sabnzbd+ run
        sabnzbd_run()
    else:
        cron_run()

