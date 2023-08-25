from abc import get_cache_token
from time import time
from DBOps import DBOps
import os
import json
from requests import get
import socket

import getpass
config_path = os.getcwd() + '/resources/params.json'


def registerMachine():
    db = DBOps()

    if getConfig('browser_mode') == None:
        query = 'SELECT name,has_command FROM modes WHERE state = 0 LIMIT 1'
        row = db.select(query)
        browser_mode = row[0][0]
        has_command = row[0][1]
        setConfig('browser_mode', browser_mode)
        setConfig('has_command', has_command)
        ip_adress = get('https://api.ipify.org').text
        query = "UPDATE modes SET state=1, IP='" + \
            ip_adress + "' WHERE name='" + browser_mode + "'"
        db.exec(query)
    else:
        print('Machine already registered!')


def getMode():

    if os.name == 'nt':
        # return "chrome_interaction_ger"
        return "windows" 

    """
    OpenWPM native EU
    OpenWPM native USA (?: evtl. mit Accept all)
    Unser Tool (Accept All)
    Consent-O-Matic (Alles ablehnen)
    Consent-O-Matic (Alles annehmen)
    I dont care about cookies
    Ninja Cookie
    Cookieblock
    Super Agent
    """ 
    if socket.gethostname() == "measurement-1":
        return "openwpm_native_eu"
    if socket.gethostname() == "measurement-2" or socket.gethostname() == "measurement-10" :
        return "openwpm_native_usa"
    if socket.gethostname() == "measurement-3":
        return "openwpm_customall_eu"
    if socket.gethostname() == "measurement-4":
        return "openwpm_omaticno_eu"
    if socket.gethostname() == "measurement-5":
        return "openwpm_omaticall_eu"
    if socket.gethostname() == "measurement-6":
        return "openwpm_dontcare_eu"
    if socket.gethostname() == "measurement-7":
        return "openwpm_ninja_eu"
    if socket.gethostname() == "measurement-8":
        return "openwpm_cookieblock_eu"
    if socket.gethostname() == "measurement-9":
        return "openwpm_superagent_eu" 
    return 0 


def getConfig(name):
    params = {
        "bigquery_insert_rows": 500,
        "has_command": False,
        "thread_count": 20,
        "browser_mode_": "openwpm_desktop_ger",
        "browser_mode": "chrome_desktop_ger",
        "subpage_to_visit": 15,
        "timeout": 30,
        "timeout_site": 1800,
        "timeout_site_min": 30,
        "time_to_sleep": 1,
        "process_name_chrome": "/home/" + getpass.getuser() +"/miniconda3/envs/openwpm/bin/python3 CrawlerChrome.py",
        "process_name_openwpm": "/home/" + getpass.getuser() +"/miniconda3/envs/openwpm/bin/python3 CrawlerOpenWPM.py",
        "resolution": [1920, 1080],
        "resolution_mobile_openwpm": [760, 360],
        "user_agent_chrome":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "user_agent_openwpm":"Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "user_agent_mobile_openwpm": "Mozilla/5.0 (Android 11; Mobile; rv:87.0) Gecko/87.0 Firefox/87.0",
        "user_agent_mobile_chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "modes": [
            "openwpm_interaction_old",
            "openwpm_interaction_1",
            "openwpm_interaction_2",
            "openwpm_desktop",
            "openwpm-headless_interaction"            
        ],
        "support_vpn":False

    }
    return params[name] 


def setConfig(name, value):
    with open(config_path) as f:
        configs = json.load(f)
    configs[name] = value
    with open(config_path, 'w') as f:
        json.dump(configs, f)


def getDriverPath():
    path = ''
    if os.name == 'nt':
        path = os.getcwd() + '/drivers/chromedriver.exe'
    else:
        path = os.getcwd() + '/drivers/chromedriver'
    return path

def getWorkspacePath():
    return os.getcwd()
 
"""
10.0.12.170	openwpm_interaction_old
10.0.12.171	openwpm_interaction_1
10.0.12.172	openwpm_interaction_2
10.0.12.173	openwpm_desktop
10.0.12.174	headless_interaction
"""
