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
    for link in sublinks:
        if name in link:
            return link

def get_job_name(loc):
    if '/' in loc:
        return os.path.splitext(loc[loc.rfind('/') + 1:])[0]
    else:
        return loc
