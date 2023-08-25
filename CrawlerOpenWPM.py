import builtins
from csv import excel_tab
from Commander_extract_Subpages import start
from datetime import datetime, timedelta
from logging import root
from Ops import addTime2Datetime, delFolder, isThirdParty, terminateProcessBySiteID, visitLogNew, visitLogNew_Full
from setup import getMode
from PushOps import pushError, stream2BQ
from Objects import VisitData, SiteData, QueueItem
import sqlite3
import os
import time
import tldextract
import sys
from DBOps import DBOps


import threading
from adblockparser import AdblockRules

rules = None               

param_root_site_url = ''
param_root_site_id = ''


# HERE WE START TO FETCH DATA FROM OPENWPM-SQLITE


def getCookies(root_site_id, root_site_url):
    try: 
        query_update = """
         ALTER TABLE javascript_cookies ADD   in_cookiejar integer;
		
        update javascript_cookies
        set in_cookiejar=1 where id in(
        select id
        from (select * from javascript_cookies j inner join ( select name, host from (select * from javascript_cookies c inner join 
        (select name, host from javascript_cookies  group by name, host ) gc on gc.name=c.name and c.host=gc.host 
        WHERE gc.name in(select name from javascript_cookies j where j.name=gc.name and j.host=gc.host and j.record_type != 'deleted' order by time_stamp desc limit 1)
        ) group by name, host) as r_cookies where id in (select id from javascript_cookies tmp where r_cookies.name=tmp.name and r_cookies.host=tmp.host order by id desc limit 1) 
        and j.record_type!='deleted') as c inner join site_visits as s on s.visit_id = c.visit_id);
		
		
            """ 
        getSQLItems(query_update, root_site_id, is_script=True)

        query = """
		select expiry, is_secure, is_http_only, same_site, name, host, path, time_stamp, c.visit_id, value, first_party_domain, is_session, is_host_only, s.site_rank, record_type, change_cause, in_cookiejar	
            from javascript_cookies as c inner join site_visits as s on s.visit_id = c.visit_id;
            """
        rows = getSQLItems(query, root_site_id)
 
        cookieList = []

        for r in rows:
            cookie = {}
            cookie['expiry'] = addTime2Datetime(r[0], 2)
            cookie['is_secure'] = r[1]
            cookie['is_http_only'] = r[2]
            cookie['same_site'] = r[3]
            cookie['name'] = r[4]
            cookie['host'] = r[5]
            cookie['path'] = r[6]
            cookie_date = r[7]
            # timedelta(hours=2)
            cookie['time_stamp'] = addTime2Datetime(r[7], 2)
            cookie['site_id'] = root_site_id  # r[8] #by openwpm
            cookie['is_host_only'] = r[12]
            cookie['is_session'] = r[11]
            cookie['value'] = r[9]
            cookie['is_third_party'] = isThirdParty(root_site_url, r[10]) 
            cookie['record_type'] = r[14]
            cookie['change_cause'] = r[15]
            cookie['in_cookiejar'] = r[16]

            cookie['visit_id'] = str(root_site_id) + '_' + str(r[13])

            cookie['browser_id'] = getMode()
            cookieList.append(cookie)
        return cookieList
    except:
        pushError(root_site_id, 'getCookies')


def getRequests(root_site_id, root_site_url, visit_id, subpage_id):
    try:
        query = "SELECT method, headers, url, time_stamp, is_XHR, referrer, post_body, browser_id, visit_id, is_third_party_channel, is_third_party_to_top_window, resource_type, top_level_url, window_id, tab_id, frame_id, parent_frame_id, frame_ancestors,  request_id, triggering_origin, loading_origin, loading_href, req_call_stack, post_body, post_body_raw FROM http_requests WHERE visit_id=" + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        reqList = []
        for r in rows:
            req = {}
            req['method'] = r[0]
            req['headers'] = r[1]
            req['url'] = r[2]
            req['time_stamp'] = addTime2Datetime(r[3], 2)
            req['is_XHR'] = r[4]
            req['referrer'] = r[5]
            req['body'] = r[6]

            req['is_third_party_channel'] = isThirdParty(
                root_site_url, r[2])  # req['is_third_party_channel'] = r[9]

            req['is_third_party_to_top_window'] = r[10]

            req['resource_type'] = r[11]
            if r[11] == 'websocket':
                req['is_websocket'] = 1
            else:
                req['is_websocket'] = 0
            req['top_level_url'] = r[12]
            req['window_id'] = r[13]
            req['tab_id'] = r[14]
            req['frame_id'] = r[15]
            req['parent_frame_id'] = r[16]
            req['frame_ancestors'] = r[17]
            req['request_id'] = r[18]
            req['triggering_origin'] = r[19]
            req['loading_origin'] = r[20]
            req['loading_href'] = r[21]
            req['req_call_stack'] = r[22]
            req['post_body'] = r[23]
            req['post_body_raw'] = r[24]

            req['site_id'] = root_site_id
            req['visit_id'] = str(root_site_id)+'_'+str(subpage_id)
            req['subpage_id'] = subpage_id
            req['browser_id'] = getMode()
            """"
            while(rules==None):
                time.sleep(0.3)
            try:
                req['is_tracker'] = int(rules.should_block(r[2]))
            except:
                pass
            """
            etld = tldextract.extract(r[2])
            req['etld'] = etld.domain + '.' + etld.suffix

            reqList.append(req)
        return reqList
    except:
        pushError(root_site_id, 'getRequests')


def pushCrawlHistory(root_site_id, visit_id, subpage_id, url):
    try:
        query = "SELECT command_status, duration, dtg from crawl_history WHERE command= 'GetCommand' and visit_id=" + \
            str(visit_id)

        rows = getSQLItems(query, root_site_id)
        for item in rows:
            crawl_state = item[0]
            timeout = 0
            if crawl_state == 'ok':
                crawl_state = 1
                timeout = 0
            elif crawl_state == 'timeout':
                crawl_state = 1
                timeout = 1
            else:
                crawl_state = -1
                timeout = 0

            start_time = addTime2Datetime(item[2], 2)

            duration = item[1]
            print(duration)

            finish_time = addTime2Datetime(start_time, duration, 'millisecond')

            visitLogNew_Full(root_site_id, url, subpage_id,
                             start_time, finish_time, timeout, crawl_state)

    except:
        pushError(root_site_id, 'getCrawlHistory')


def getResponses(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT method, headers, url, time_stamp, response_status, response_status_text, browser_id, visit_id, content_hash, request_id FROM http_responses WHERE visit_id=" + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        resList = []
        for r in rows:
            res = {} 

            res['method'] = r[0]
            res['headers'] = r[1]
            res['url'] = r[2]
            res['time_stamp'] = addTime2Datetime(r[3], 2)
            res['response_status'] = r[4]
            res['response_status_text'] = r[5]
            res['content_hash'] = r[8]
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)

            etld = tldextract.extract(r[2])
            res['etld'] = etld.domain + '.' + etld.suffix

            res['content_hash'] = r[9]
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()

            resList.append(res)

        return resList
    except:
        pushError(root_site_id, 'getResponses')



def getLocalStorage(root_site_id):
    """
    try:
        path = getProfileFolder(root_site_id) + '/localStorage.txt'

        if not os.path.isfile(path):
            return None

        with open(path) as f:
            data = f.read()
        import ast
        storage = ast.literal_eval(data)
        locList = []

        for k, v in storage.items():
            ls = {}
            ls['browser_id'] = getMode()
            ls['key'] = k
            ls['value'] = v
            ls['site_id'] = root_site_id
            locList.append(ls) 

        return locList
    except:
        pushError(root_site_id, 'getLocalStorage')
    """

    try:
        dist= "./profiles/openwpm/" + str(root_site_id) + "/webappsstore.sqlite"
        if not os.path.isfile(dist): 
            return None
        
        query= "SELECT originAttributes, originKey, scope, key, value FROM webappsstore2"

        sqliteConnection = sqlite3.connect(dist)
        cursor = sqliteConnection.cursor()
        rows = cursor.execute(query).fetchall()
        sqliteConnection.close()


        locList = []
        for r in rows:
            res = {}
            res['origin_attributes'] = r[0]
            res['origin_key'] = r[1]
            res['scope'] = r[2]
            res['key'] = r[3]
            res['value'] = r[4] 
            res['browser_id'] = getMode()
            res['site_id'] = str(root_site_id)

            locList.append(res)

        return locList 
    except Exception as e:
        
        pushError(root_site_id, 'LocalStorageRead()')
        print(e)
        
 


def getCallStacks(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT request_id, browser_id, visit_id, call_stack from callstacks WHERE visit_id=" + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        stackList = []
        for r in rows:
            res = {}
            res['request_id'] = r[0]
            res['browser_id'] = r[1]
            res['visit_id'] = r[2]
            res['call_stack'] = r[3]
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()

            stackList.append(res)

        return stackList
    except:
        pushError(root_site_id, 'getCallStacks')


def getDnsResponses(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT request_id, browser_id, visit_id, hostname, addresses, used_address, canonical_name, is_TRR, time_stamp from dns_responses WHERE visit_id= " + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        dnsList = []
        for r in rows:
            res = {}
            res['request_id'] = r[0]
            res['browser_id'] = r[1]
            # res['request_id'] = r[2] # we don't need this
            res['hostname'] = r[3]
            res['addresses'] = r[4]
            res['used_address'] = r[5]
            res['canonical_name'] = r[6]
            res['is_TRR'] = r[7]
            res['time_stamp'] = addTime2Datetime(r[8], 2)
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()

            dnsList.append(res)

        return dnsList
    except:
        pushError(root_site_id, 'getDnsResponses')


def getHttpRedirects(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT incognito, browser_id, old_request_url, old_request_id, new_request_url, window_id, tab_id, frame_id, response_status, response_status_text, headers, time_stamp from http_redirects WHERE visit_id= " + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        redList = []
        for r in rows:
            res = {}
            res['incognito'] = r[0]
            # res['browser_id'] = r[1] # we don't need this
            res['old_request_url'] = r[2]
            res['old_request_id'] = r[3]
            res['new_request_url'] = r[4]
            res['window_id'] = r[5]
            res['tab_id'] = r[6]
            res['frame_id'] = r[7]
            res['response_status'] = r[8]
            res['response_status_text'] = r[9]
            res['headers'] = r[10]
            res['time_stamp'] = addTime2Datetime(r[11], 2)
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()
            redList.append(res)

        return redList
    except:
        pushError(root_site_id, 'getHttpRedirects')


def getIncompleteVisits(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT visit_id from incomplete_visits WHERE visit_id= " + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        redList = []
        for r in rows:
            res = {}
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()
            redList.append(res)

        return redList
    except:
        pushError(root_site_id, 'getIncompleteVisits')


def getJavascript(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT visit_id from incomplete_visits WHERE visit_id= " + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        jsList = []
        for r in rows:
            res = {}

            res['incognito'] = r[0]
            res['event_ordinal'] = r[1]
            res['page_scoped_event_ordinal'] = r[2]
            res['window_id'] = r[3]
            res['tab_id'] = r[4]
            res['frame_id'] = r[5]
            res['script_url'] = r[6]
            res['script_line'] = r[7]
            res['script_col'] = r[8]
            res['func_name'] = r[9]
            res['script_loc_eval'] = r[10]
            res['document_url'] = r[11]
            res['top_level_url'] = r[12]
            res['call_stack'] = r[13]
            res['symbol'] = r[14]
            res['operation'] = r[15]
            res['value'] = r[16]
            res['arguments'] = r[17]
            res['time_stamp'] = addTime2Datetime(r[18], 2)
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()
            jsList.append(res)

        return jsList
    except:
        pushError(root_site_id, 'getJavascript')


def getNavigations(root_site_id, visit_id, subpage_id):
    try:
        query = "SELECT id,incognito,browser_id,visit_id,extension_session_uuid,process_id,window_id,tab_id,tab_opener_tab_id,frame_id,parent_frame_id,window_width,window_height,window_type,tab_width,tab_height,tab_cookie_store_id,uuid,url,transition_qualifiers,transition_type,before_navigate_event_ordinal,before_navigate_time_stamp,committed_event_ordinal,committed_time_stamp from navigations WHERE visit_id= " + \
            str(visit_id)
        rows = getSQLItems(query, root_site_id)
        jsList = []
        for r in rows:
            res = {}

            res['incognito'] = r[0]
            #res['browser_id'] = r[1]
            #res['visit_id'] = r[2]
            res['extension_session_uuid'] = r[3]
            res['process_id'] = r[4]
            res['window_id'] = r[5]
            res['tab_id'] = r[6]
            res['tab_opener_tab_id'] = r[7]
            res['frame_id'] = r[8]
            res['parent_frame_id'] = r[9]
            res['window_width'] = r[10]
            res['window_height'] = r[11]
            res['window_type'] = r[12]
            res['tab_width'] = r[13]
            res['tab_height'] = r[14]
            res['tab_cookie_store_id'] = r[15]
            res['uuid'] = r[16]
            res['url'] = r[17]
            res['transition_qualifiers'] = r[18]
            res['transition_type'] = r[19]
            res['before_navigate_event_ordinal'] = r[20]
            res['before_navigate_time_stamp'] = r[21]
            res['committed_event_ordinal'] = r[22]
            res['committed_time_stamp'] = r[23]
            res['visit_id'] = str(root_site_id) + '_' + str(subpage_id)
            res['site_id'] = root_site_id
            res['subpage_id'] = subpage_id
            res['browser_id'] = getMode()
            jsList.append(res)

        return jsList
    except:
        pushError(root_site_id, 'getNavigations')


def loadVisitList(root_site_id, root_site_url):
    visitList = []
    try:
        # site rank used as subpage_id
        query = 'SELECT visit_id, site_url, site_rank from site_visits'
        rows = getSQLItems(query, root_site_id)

        for r in rows:
            subpage_id = r[2]
            url = r[1]
            visit_id_openwpm = r[0]  # that assigned by openwpm
            visit = VisitData(url)

            visit.requests = getRequests(
                root_site_id, root_site_url, visit_id_openwpm, subpage_id)
            visit.responses = getResponses(
                root_site_id, visit_id_openwpm, subpage_id) 

            visit.callstacks = getCallStacks(
                root_site_id, visit_id_openwpm, subpage_id)
            visit.dns_responses = getDnsResponses(
                root_site_id, visit_id_openwpm, subpage_id)
            visit.http_redirects = getHttpRedirects(
                root_site_id, visit_id_openwpm, subpage_id)
            visit.incomplete_visit = getIncompleteVisits(
                root_site_id, visit_id_openwpm, subpage_id)
            #visit.javascript = getJavascript(
            #    root_site_id, visit_id_openwpm, subpage_id)
            visit.navigations = getNavigations(
                root_site_id, visit_id_openwpm, subpage_id)

            pushCrawlHistory(root_site_id, visit_id_openwpm, subpage_id, url)

            visit.subpage_id = subpage_id
            visit.root_url = root_site_url
            visit.visit_id = str(root_site_id) + '_' + str(subpage_id)
            if r[2] == 0:
                visit.subpage = False
            else:
                visit.subpage = True
            visitList.append(visit)
    except:
        pushError(root_site_id, 'loadCrawlList()')

    return visitList


def getSQLItems(query, root_site_id, is_script=False):
    try:
        sqliteConnection = sqlite3.connect(getProfilePath(root_site_id))
        cursor = sqliteConnection.cursor() 

        if is_script:
            rows = cursor.executescript(query).fetchall()
        else:
            rows = cursor.execute(query).fetchall()
        sqliteConnection.close()
        return rows
    except Exception as e:
        pushError(root_site_id, 'getSQLItems()')
        print(e)


def getProfilePath(root_site_id):
    path = os.getcwd() + '/profiles/openwpm/' + \
        str(root_site_id) + '/crawl-data.sqlite'  # FIXME
    return path


def getProfileFolder(root_site_id):
    path = os.getcwd() + '/profiles/openwpm/' + str(root_site_id)
    return path


def runWrapper(p_queue, q_item):
    root_site_id = q_item.site_ID
    try:
        deleteProfileData(root_site_id)
    except:
        pushError(q_item.site_id, 'deleteProfileData()')
        pass

    from CrawlerOpenWPM_Wrapper import initiliaze_openwpm
    initiliaze_openwpm(p_queue, q_item)


def deleteProfileData(root_site_id):
    if os.path.exists(getProfileFolder(root_site_id)):
        import shutil
        try:
            shutil.rmtree(getProfileFolder(root_site_id))
        except OSError as e:
            pushError(root_site_id, 'deleteProfileData()')
            pass


def changeSiteState(siteID, state, timeout=0):
    query = "UPDATE sites SET state_{} = {}, timeout={}  where id = {} ".format(
        getMode(), state, timeout, siteID)
    print(query)
    db.exec(query)


def runOpenWPMInstance(p_queue, p_queue_item):
    """
    t = threading.Thread(target=loadRules)
    t.start()
    """
    root_site_id = p_queue_item.site_ID
    root_site_url = p_queue_item.url

    siteData = SiteData()
    siteData.browser_id = getMode()
    siteData.site_id = root_site_id

    try:

        runWrapper(p_queue, p_queue_item)

        siteData.visitData = loadVisitList(root_site_id, root_site_url)
        siteData.cookies = getCookies(root_site_id, root_site_url)


        try:
            siteData.localStorage = getLocalStorage(root_site_id)
        except:
            pushError(root_site_id, 'openwpm_localstorage')
            pass

        try:
            stream2BQ(siteData)
        except:
            pushError(root_site_id, 'openwpm_BQ')
            if siteData is None:
                pushError(root_site_id, 'openwpm_BQ_isNone')
            pass

        delFolder(getProfileFolder(root_site_id))  

        siteData.state = 2
        siteData.state_text = 'successful'
    except Exception as e:
        print(e)
        # -1: not startet, 0:waiting , 1: crawling , 2: success, 3: error, 4 timeout
        siteData.state = 3
        siteData.state_text = 'error'
        pushError(root_site_id, 'openwpm_crawler')
    finally:
        changeSiteState(root_site_id, siteData.state)

    return siteData


def terminateProcess(id):
    terminateProcessBySiteID(id)
    exit(0)


if __name__ == "__main__":
    import sys
    id = sys.argv[1]
    ready = False
    try:
        ready = eval(sys.argv[2])
    except:
        pass
    import sys
    db = DBOps()
    while(not ready):
        query = "SELECT 1 FROM sites WHERE ready IS TRUE and id=" + \
            str(id)
        rows = db.select(query)
        if len(rows) > 0:
            print('Site ready, so i restart!')
            import subprocess
            import getpass
            subprocess.Popen(['/home/' + getpass.getuser() +'/miniconda3/envs/openwpm/bin/python3',
                              'CrawlerOpenWPM.py', str(id), str(True),  str(datetime.now())])
            os.system('kill %d' % os.getpid())
            print(' I terminate')
            exit(0)
        else:
            query = "SELECT 1 FROM sites WHERE state_openwpm_native_eu = 0 and   state_openwpm_native_usa = 0 and   state_openwpm_customall_eu = 0 and   state_openwpm_omaticno_eu = 0 and   state_openwpm_omaticall_eu = 0 and   state_openwpm_dontcare_eu = 0 and   state_openwpm_ninja_eu = 0 and   state_openwpm_cookieblock_eu = 0 and state_openwpm_superagent_eu= 0  AND id=" + \
                str(id)
            rows = db.select(query)
            if len(rows) != 0:
                query = "UPDATE sites SET ready=true WHERE id=" + \
                    str(id)
                db.exec(query)
            time.sleep(3)
            continue

    r = db.select(
        'select id,  concat(scheme, site), subpages from sites where id= '+str(sys.argv[1]))[0]
    queue_item = QueueItem(r[0], r[1], 'waiting', r[2], None, None, None)
    changeSiteState(id, 1)
    runOpenWPMInstance(None, queue_item)
    print('finish:', queue_item.url)
    os.system('kill %d' % os.getpid())
