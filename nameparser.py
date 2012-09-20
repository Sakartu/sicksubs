import re
import os

# regexes are in order of importance
rexes = ['(S(\d\d)E(\d\d))', '((\d{1,2})x(\d{1,2}))', '\D((\d)(\d\d))\D']
hd_quals = ['720p', '1080p', '1080i']
sd_quals = ['HDTV']
quals = hd_quals + sd_quals
video_exts = [u'mkv', u'avi', u'mpg', u'mpeg', u'mp4', u'mov']


def get_ep_details(line):
    for rex in rexes:
        c = re.compile(rex, re.I)
        m = c.search(line)
        if m:
            try:
                # S01E02, 01, 02
                return (m.group(1), int(m.group(2)), int(m.group(3)))
            except:
                return (None, None)


def find_link(name, sublinks):
    if not sublinks:
        return None

    # match the full name if we can
    for link in sublinks:
        if name.lower() in link.lower():
            return link

    grp = get_release_group(name)
    (seline, s, e) = get_ep_details(name)

    # if not, search for group, season, ep and quality identifier
    for link in sublinks:
        if (grp.lower() in link.lower()
        and get_quality(name) == get_quality(link)):
            # group and quality match, check for season and ep
            _, other_s, other_e = get_ep_details(link)
            if seline.lower() in link.lower():
                return link
            elif other_s == s and other_e == e:
                return link

    # return nothing if it can't be found
    return None


def get_release_group(name):
    '''
    Get the release group from a name. For instance, in the case of
    lost.girl.s02e11.hdtv.xvid-2hd.avi
    returns '-2hd'
    '''
    if '-' in name:
        return name[name.rfind('-'):]
    else:
        return name


def get_quality(name):
    '''
    Outputs the quality of a name, hightest quality first.
    '''
    for qual in quals:
        if qual.lower() in name.lower():
            return qual

    return None


def get_job_name(loc):
    if '/' in loc:
        return os.path.splitext(loc[loc.rfind('/') + 1:])[0]
    else:
        return loc


def filter_qual(subs, hd):
    '''
    This helper function first splits the given sub tuples in hd and sd subs
    and then returns one of both possibilities given the hd param
    '''
    sds = []
    hds = []
    for s in subs:
        if get_quality(s[0]) in hd_quals:
            hds.append(s)
        else:
            sds.append(s)
    if hd:
        return hds
    else:
        return sds
