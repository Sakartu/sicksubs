#!/usr/bin/python
import db
import os
import sys
import glob
import shlex
import sqlite3
import urllib2
import bierdopje
import subprocess
import nameparser


def main():
    if sys.argv[1:]:
        showname = ' '.join(sys.argv[1:])
    else:
        showname = raw_input(u'What show would you like subs for? ')
    showinfos = bierdopje.find_shows_by_name(showname)

    maxlen = max(map(lambda x: len(x[0]), showinfos))
    showlist = 'id.   ' + 'Name'.ljust(maxlen) + '   Aired\n'
    for i, (name, firstaired, sid, seasons) in enumerate(showinfos):
        if not firstaired:
            firstaired = '?'
        showlist += '{id:02d}.   {name:{maxlen}s}   {firstaired}\n'.format(
                id=i + 1,
                maxlen=maxlen,
                name=name,
                firstaired=firstaired)

    print showlist
    answer = raw_input(u'Which show (id) would you like me to download subs '
    'for? ')
    try:
        show = showinfos[int(answer) - 1]
        sid = show[2]
    except:
        print u'Invalid id chosen or server returned garbage!'
        sys.exit(-1)
    try:
        s = raw_input(u'For which season would you like to download subs, '
                '[{0}-{1}]? '.format(1, int(show[3])))
    except:
        print u'Invalid season provided!'
        sys.exit(-1)

    lang = raw_input(u'Which lang would you like to download subs for? '
    '[en] ').strip()
    if lang not in ('nl', 'en'):
        lang = 'en'

    all_subs = bierdopje.get_subs_by_season(sid, lang, s)
    to_download = []
    maxsub = max(all_subs)
    e = 1
    while e <= maxsub:
        sublist = ''
        for i, (name, link) in enumerate(all_subs[e]):
            sublist += '{id:02d}.   {name}\n'.format(id=i + 1, name=name)
        print sublist
        try:
            answer = int(raw_input(u'Which sub (id) would you like me to '
            'download? '))
            if answer < 1 or answer > (i + 1):
                raise Exception
            to_download.append(all_subs[e][answer - 1])
        except KeyboardInterrupt:
            print u'Aborting...'
            sys.exit(-1)
        except:
            print u'Garbage or too large id given, continuing with next'
        e += 1
    print u'Downloading...'
    for d in to_download:
        download(d)


def download(sub):
    '''
    This helper method downloads all the files to the current directory
    '''
    name, link = sub
    try:
        resp = urllib2.urlopen(link)

        content = resp.read()
        sub_path = './' + name
        with open(sub_path, 'w+') as sub:
            sub.write(content)
            print "Successfully downloaded sub {0}".format(name)
    except Exception, e:
        print "Couldn't download sub {0}".format(name)
        print e
        return False
    return True


if __name__ == '__main__':
    main()
