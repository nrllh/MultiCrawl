from pathlib import Path
 
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager
from custom_command import TMP, CopyLocalStorage, DetectBannerCommand, LoadLocalStorage


import builtins

builtins.cookieButtons = {} 
builtins.localStorage={} 


# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = [
    "https://yahoo.de", 
]

# Loads the default ManagerParams
# and NUM_BROWSERS copies of the default BrowserParams

manager_params = ManagerParams(num_browsers=NUM_BROWSERS)
browser_params = [BrowserParams(display_mode="native") for _ in range(NUM_BROWSERS)]

print(browser_params[0].profile_archive_dir)

# Update browser configuration (use this for per-browser settings)
for browser_param in browser_params:
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

    browser_param.profile_archive_dir=Path("./profiles/openwpm/" + str(987))


# Update TaskManager configuration (use this for crawl-wide settings)
manager_params.data_directory = Path("./datadir/")
manager_params.log_path = Path("./datadir/openwpm.log")

# memory_watchdog and process_watchdog are useful for large scale cloud crawls.
# Please refer to docs/Configuration.md#platform-configuration-options for more information
# manager_params.memory_watchdog = True
# manager_params.process_watchdog = True


# Commands time out by default after 60 seconds
with TaskManager(
    manager_params,
    browser_params,
    SQLiteStorageProvider(Path("./datadir/crawl-data.sqlite")),
    None,
) as manager:
    # Visits the sites
    for index, site in enumerate(sites):

        def callback(success: bool, val: str = site) -> None:
            print(
                f"CommandSequence for {val} ran {'successfully' if success else 'unsuccessfully'}"
            )

        # Parallelize sites over all number of browsers set above.
        command_sequence = CommandSequence(
            site,
            site_rank=index,
            callback=callback,
        )

        # Start by visiting the page
        command_sequence.append_command(GetCommand(url=site, sleep=5), timeout=20)
        # Have a look at custom_command.py to see how to implement your own command 

        command_sequence.append_command(DetectBannerCommand(site, 1))
        #command_sequence.append_command(LoadLocalStorage(1))
        command_sequence.append_command(CopyLocalStorage(1))
 

        # Run commands across all browsers (simple parallelization)
        manager.execute_command_sequence(command_sequence)
