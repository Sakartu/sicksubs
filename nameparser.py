import re
import os
rexes = ['S(\d\d)E(\d\d)', '(\d{1,2})x(\d{1,2})', '(\d)(\d\d)'] #in order

def get_ep_details(line):
    for rex in rexes:
        c = re.compile(rex, re.I)
        m = c.search(line)
        if m:
            try:
                return (int(m.group(1)), int(m.group(2)))
            except:
                return (None, None)

def find_link(name, sublinks):
    if not sublinks:
        return None
    grp = get_release_group(name)
    for link in sublinks:
        if grp in link:
            return link

def get_release_group(name):
    '''
    Get the release group from a name. For instance, in the case of 
    lost.girl.s02e11.hdtv.xvid-2hd.avi
    returns '-2hd'
    '''
    name = os.path.splitext(name)[0]
    if name:
        return name[name.rfind('-'):]
    else:
        return name

def get_job_name(loc):
    if '/' in loc:
        return os.path.splitext(loc[loc.rfind('/') + 1:])[0]
    else:
        return loc
