import urllib
import urllib2
from xml.dom import minidom

API_KEY = u'6935AC4D8CF45C7A'
API = u'http://api.bierdopje.com/{key}/'.format(key=API_KEY)
FEED = u'http://feeds.bierdopje.com/bierdopje/subs/english'
SID_BY_TVDBID = API + 'GetShowByTVDBID/{sid}'
SUBS_BY_EP = API + 'GetAllSubsFor/{sid}/{s}/{e}/{lang}'


def get_show_id(sid):
    '''
    Helper method to find a bierdopje show_id for a given showname
    '''
    url = SID_BY_TVDBID.format(sid=urllib.quote(sid))
    data = get_content(url, 'showid')
    if data:
        return data[0].firstChild.data
    else:
        return None

def get_subs(showid, lang, season, ep):
    url = SUBS_BY_EP.format(sid=showid, s=season, e=ep, lang=lang)
    data = get_content(url, 'downloadlink')
    # since bierdopje sometimes shifts the epnumbers around, we also check
    # the previous ep
    url = SUBS_BY_EP.format(sid=showid, s=season, e=ep - 1, lang=lang)
    if data:
        more_data = get_content(url, 'downloadlink')
        if more_data:
            data = data + more_data
    if data:
        return [x.firstChild.data for x in data]
    else:
        return []

def get_content(url, tag):
    try:
        req = urllib2.urlopen(url)
        dom = minidom.parse(req)
        req.close()
    except:
        return None
    
    if not dom or len(dom.getElementsByTagName(tag)) == 0 :
        return None
    
    return dom.getElementsByTagName(tag)
