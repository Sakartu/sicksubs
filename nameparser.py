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

def find_link(job, sublinks):
    for link in sublinks:
        if job.job_name in link:
            return link
