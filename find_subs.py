#!/usr/bin/python
import os
import sys
import urllib2
import bierdopje
import nameparser


def main():
    try:
        if sys.argv[1:]:
            showname = ' '.join(sys.argv[1:])
        else:
            showname = raw_input(u'What show would you like subs for? ')
        showinfos = bierdopje.find_shows_by_name(showname)

        if not showinfos:
            print u'Could not find show "{0}"!'.format(showname)
            return

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
        answer = raw_input(u'Which show (id) would you like me to download '
        'subs for? ')
        try:
            show = showinfos[int(answer) - 1]
            sid = show[2]
        except:
            print u'Invalid id chosen or server returned garbage!'
            sys.exit(-1)
        try:
            s = int(raw_input(u'For which season would you like to download '
            'subs, [{0}-{1}]? '.format(1, int(show[3]))))
            if s < 1 or s > int(show[3]):
                raise Exception
        except:
            print u'Invalid season provided!'
            sys.exit(-1)

        lang = raw_input(u'Which lang would you like to download subs for '
        '(en/nl)? [en] ').lower().strip()
        if lang not in ('nl', 'en'):
            print u'Invalid choice, defaulting to "en"'
            lang = 'en'

        qual = raw_input(u'Do you prefer HD rips? [yes] ').lower().strip()
        hd = ('y' in qual or qual.strip() == '')

        answer = raw_input(u'Do you want to download all available '
        'subs? [no] ')
        download_all = 'y' in answer.lower()

        all_subs = bierdopje.get_subs_by_season(sid, lang, s)
        to_download = []
        maxsub = max(all_subs)
        e = 1
        while e <= maxsub:
            try:
                if e not in all_subs:
                    print u'Could not find subs for ep number {0}!'.format(e)
                    continue

                possibles = nameparser.filter_qual(all_subs[e], hd)
                if not possibles:
                    print u'Could not find subs for ep number {0}!'.format(e)
                    continue

                if download_all:
                    to_download.extend(possibles)
                    continue

                if len(possibles) == 1:
                    # only one choice, download immediately
                    print (u'Only one choice for ep number {0}, will download '
                    '{1}!').format(e, possibles[0][0])
                    to_download.append(possibles[0])
                    continue
                print (u'Multiple choices for ep number {0}, please pick '
                'one:').format(e)
                for i, (name, link) in enumerate(possibles):
                    print '{id:02d}.   {name}'.format(
                            id=i + 1,
                            name=name)
                answer = None
                while answer < 1 or answer > (i + 1):
                    try:
                        answer = int(raw_input(u'Which sub (id) would you '
                            'like me to download? '))
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt
                    except:
                        print u'That\'s not a number!'
                to_download.append(possibles[answer - 1])
            finally:
                e += 1

        print u'Downloading...'

        for d in to_download:
            download(d)

        print u'Download complete!'
    except KeyboardInterrupt:
        print u'Aborting...'
        sys.exit(-1)


def download(sub):
    '''
    This helper method downloads all the files to the current directory
    '''
    name, link = sub
    try:
        resp = urllib2.urlopen(link)

        if 'content-disposition' in resp.info().dict:
            filename = resp.info().dict['content-disposition']
            subext = os.path.splitext(filename)[1]
        else:
            subext = '.srt'

        content = resp.read()
        sub_path = './' + name + subext
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
