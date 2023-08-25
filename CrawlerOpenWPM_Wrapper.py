
from Ops import visitLogUpdate
from Objects import QueueItem
from pathlib import Path

from custom_command import ChangeRes, CopyLocalStorage, InstallExtension, LoadMobileConfigs, DoInteraction, LoadLocalStorage, LogVisit, DetectBannerCommand
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager
from random import randrange
from setup import getConfig, getMode
import os
from datetime import datetime


def initiliaze_openwpm(p_queue, q_item):

    site_ID = str(q_item.site_ID)

    sites = []
    sites.append([0, q_item.url])

    if getConfig('subpage_to_visit') != 0:
        if q_item.subpages is not None:
            subs = q_item.subpages
            subs = subs.split('\n')

            for index, item in enumerate(subs):
                if index<getConfig('subpage_to_visit'):
                    sites.append([index + 1, item])

    NUM_BROWSERS = 1
    manager_params = ManagerParams(num_browsers=1)

    
    browser_params = [BrowserParams(display_mode=getDisplayMode(), prefs={
                                        "general.useragent.override": getConfig('user_agent_openwpm')}) for _ in range(NUM_BROWSERS)]

    if isMobile():
        browser_params = [BrowserParams(display_mode=getDisplayMode(), prefs={
                                        "general.useragent.override": getUserAgentMobile()}) for _ in range(NUM_BROWSERS)]
    else:
        browser_params = [BrowserParams(
            display_mode=getDisplayMode()) for _ in range(NUM_BROWSERS)]

    for browser_param in browser_params:
        
        #Bot mitigation
        browser_param.bot_mitigation=True
        # Record HTTP Requests and Responses
        browser_param.http_instrument = True
        # Record cookie changes
        browser_param.cookie_instrument = True
        # Record Navigations
        browser_param.navigation_instrument = True
        # Record JS Web API calls
        browser_param.js_instrument = False
        # Record the callstack of all WebRequests made
        browser_param.callstack_instrument = False
        # Record DNS resolution
        browser_param.dns_instrument = True


    manager_params.data_directory = Path("./profiles/openwpm/" + site_ID)
    manager_params.log_directory = Path("./profiles/openwpm/" + site_ID)
    manager_params.memory_watchdog = True
    manager_params.process_watchdog = True

    # crawler starts here
    with TaskManager(
        manager_params,
        browser_params,
        SQLiteStorageProvider(
            Path("./profiles/openwpm/" + site_ID + "/crawl-data.sqlite")),
        None,
    ) as manager:
        # Visits the sites
        for index, site in enumerate(sites):
            is_success = None

            def callback(success: bool, val: str = site) -> None:
                global is_success
                is_success = success
                print(
                    f"CommandSequence for {val} ran {'successfully' if success else 'unsuccessfully'}"
                )
                if success:
                    state = 1
                else:
                    state = -1
                str()#visitLogUpdate(site_ID, site[0], state, True)

            browser_param.profile_archive_dir=Path("./profiles/openwpm/" + site_ID)

            command_sequence = CommandSequence(
                site[1],
                reset=False,  # stateless or not
                callback=callback,
                site_rank=site[0]
            )
            command_sequence.append_command(ChangeRes())

            
            # install extension only first init. 
            #if len(sites)-1 == index: 
            if index==0: 
                command_sequence.append_command(InstallExtension())

            # run site
            command_sequence.append_command(
                GetCommand(url=site[1], sleep=0), timeout=30)
 

            if index==0: 
                if fireAcceptAll():
                    command_sequence.append_command(DetectBannerCommand(site[1], site_ID))
            
            command_sequence.append_command(DoInteraction())            
 
            if len(sites)-1 == index: 
                command_sequence.append_command(LoadLocalStorage(site_ID))

            if len(sites)-1 == index: 
                command_sequence.append_command(CopyLocalStorage(site_ID))

            manager.execute_command_sequence(command_sequence)

    return is_success


def getDisplayMode():
    mode = getMode()
    browser_type = mode.split('_')[0]
    if browser_type == 'openwpmheadless':
        return "headless"
    else:
        return "native"

def fireAcceptAll():
    mode = getMode()
    browser_config = mode.split('_')[1]
    if browser_config == 'customall':
        return True
    else:
        return False

def isMobile():
    mode = getMode()
    browser_config = mode.split('_')[1]
    if browser_config == 'mobile':
        return True
    else:
        return False


def isInteraction():
    mode = getMode()
    browser_config = mode.split('_')[1]
    if browser_config == 'interaction':
        return True
    else:
        return False


def getUserAgentMobile():
    return getConfig('user_agent_mobile_openwpm')

def getUserAgent():
    return getConfig('user_agent_openwpm')


def getResolution():
    return getConfig('resolution_normal')


def runOpenWPM_via_Wrapper(sites=None):
    if sites == None:
        sites = QueueItem('11111', 'https://alibaba.com',
                          None, None, None, None,None)
    is_success = initiliaze_openwpm(sites,sites)
    return is_success
 
