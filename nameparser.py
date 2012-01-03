import re
import os
rexes = ['(S(\d\d)E(\d\d))', '((\d{1,2})x(\d{1,2}))', '((\d)(\d\d))'] #in order
quals = ['720p', '1080p', '1080i', 'HDTV']

def get_ep_details(line):
    for rex in rexes:
        c = re.compile(rex, re.I)
        m = c.search(line)
        if m:
            try:
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
    s = str(s)
    e = str(e)

    # if not, search for group, season, ep and quality identifier
    for link in sublinks:
        if grp.lower() in link.lower() and get_quality(name) == get_quality(link):
            if seline.lower() in link.lower() or (s in link 
                    and e in link[link.find(s):]):
                # group and quality match, check for season and ep
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
