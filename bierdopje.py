import nameparser
import urllib
import urllib2
from collections import defaultdict
from xml.dom import minidom

API_KEY = u'6935AC4D8CF45C7A'
API = u'http://api.bierdopje.com/{key}/'.format(key=API_KEY)
FEED = u'http://feeds.bierdopje.com/bierdopje/subs/english'
SID_BY_TVDBID = API + 'GetShowByTVDBID/{sid}'
SID_BY_NAME = API + 'FindShowByName/{name}'
SUBS_BY_EP = API + 'GetAllSubsFor/{sid}/{s}/{e}/{lang}'
SUBS_BY_SEASON = API + 'GetSubsForSeason/{sid}/{s}/{lang}'


def get_show_id(tvdbid):
    '''
    Helper method to find a bierdopje show for a given tvdbid
    '''
    url = SID_BY_TVDBID.format(sid=urllib.quote(tvdbid))
    data = get_content(url, 'showid')
    if data:
        return data[0].firstChild.data
    else:
        return None


def find_shows_by_name(name):
    '''
    Helper method to find a bierdopje show for a given name
    '''
    url = SID_BY_NAME.format(name=urllib.quote(name))
    dom = get_content(url)
    if not dom:
        return None
    names = get_datas(dom.getElementsByTagName('showname'))
    firstaired = get_datas(dom.getElementsByTagName('firstaired'))
    sids = get_datas(dom.getElementsByTagName('showid'))
    seasons = get_datas(dom.getElementsByTagName('seasons'))
    return zip(names, firstaired, sids, seasons)


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


def get_subs_by_season(showid, lang, season):
    url = SUBS_BY_SEASON.format(sid=showid, s=season, lang=lang)
    data = get_content(url)
    filenames = get_datas(data.getElementsByTagName('filename'))
    links = get_datas(data.getElementsByTagName('downloadlink'))
    eps = defaultdict(lambda: [])
    for f, l in zip(filenames, links):
        _, _, e = nameparser.get_ep_details(f)
        eps[e].append((f, l))

    return eps


def get_content(url, tag=None):
    try:
        req = urllib2.Request(url)
        req.add_header('User-agent', 'sicksubs/v1.0')
        resp = urllib2.urlopen(req)
        dom = minidom.parse(resp)
        resp.close()
    except Exception, e:
        print e
        return None

    if not dom or (tag and len(dom.getElementsByTagName(tag)) == 0):
        return None

    if tag:
        return dom.getElementsByTagName(tag)
    else:
        return dom


def get_data(dom):
    return dom.firstChild.data


def get_datas(doms):
    result = []
    for x in doms:
        try:
            result.append(x.firstChild.data)
        except:
            result.append('')
    return result
