import re
rexes = map(re.compile, ['S(\d\d)E(\d\d)', '(\d{1,2})x(\d{1,2})'])

def get_ep_details(line):
    for rex in rexes:
        m = rex.search(line)
        if m:
            try:
                return (int(m.group(1)), int(m.group(2)))
            except:
                return (None, None)

def find_link(name, sublinks):
    for link in sublinks:
        if name in link:
            return link

def get_job_name(loc):
    if '/' in loc:
        return loc[loc.rfind('/'):]
    else:
        return loc
