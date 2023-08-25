from email import header
import sys
from DBOps import DBOps
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import tldextract
from urllib.parse import urlparse, unquote
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    MoveTargetOutOfBoundsException,
    TimeoutException,
    WebDriverException,
)

import multiprocessing
from google.cloud import bigquery

thread_count = 10

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + \
    '/resources/google.json'
client = bigquery.Client()


def getSeleniumProfilePath():
    import tempfile
    dirpath = tempfile.mkdtemp()
    return dirpath

    path = ''
    if os.name == 'nt':
        path = os.getcwd() + '/profiles/chrome/main_commander/'
    else:
        path = os.getcwd() + '/profiles/chrome/main_commander/'
    return path


def loadBrowser():

    xoptions = webdriver.ChromeOptions()
    xoptions.add_argument("--log-level=3")
    profile_path = getSeleniumProfilePath()
    print(profile_path)
    xoptions.add_argument("user-data-dir=" + profile_path)
    # options.page_load_strategy = 'none'
    xoptions.add_argument("no-sandbox")
    xoptions.add_argument("disable-gpu")
    xoptions.add_argument("disable-browser-side-navigation ")
    xoptions.add_argument("headless")

    driver = webdriver.Chrome(
        executable_path=getDriverPath(), options=xoptions)

    driver.find_element
    return driver, profile_path


def getDriverPath():
    path = ''
    if os.name == 'nt':
        path = os.getcwd() + '/drivers/chromedriver.exe'
    else:
        path = os.getcwd() + '/drivers/chromedriver'
    return path


def start():
    query_tracker = """SELECT
  DISTINCT(name)
FROM
  cookies.cookies
WHERE
  name NOT IN (
  SELECT
    name
  FROM
    `ifis-web-measurements.cookies.cookies_cat_processed`)"""
    query_job = client.query(query_tracker)
    try:
        rows = query_job.result().to_dataframe().values.tolist()
        print('query data loaded.')
    except Exception as e:
        print(e)
        print('error')

    totalRow = len(rows)
    print("Total Rows: ", totalRow)
    avarageRows = int(totalRow/thread_count)

    splittedRows = []
    for i in range(thread_count):
        if i == len(range(thread_count))-1:
            splittedRows.append(rows)
        else:
            splittedRows.append(rows[0:avarageRows])
            del rows[0:avarageRows]

        print("splittedRows count: " + str(len(splittedRows)))
        print("row count: " + str(len(rows)))

    for item in splittedRows:
        p1 = multiprocessing.Process(
            target=doAnalyse, args=(item,))
        p1.start()


def doAnalyse(rows):

    cookieList = []
    for item in rows:
        cookie = {}
        cookie['name'] = item[0]
        cookie['cat'] = getCat(item[0])
        cookieList.append(cookie)
        print(cookie)
        if len(cookieList) == 50:
            pushRows('cookies.cookies_cat_processed', cookieList)
            cookieList = []


def getCat(name):

    import requests
    import re
    url = "https://cookiepedia.co.uk/cookies/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    full_url = url + name

    req = requests.get(full_url, headers=headers)
    if req.status_code != 200:
        pass

    lbl_cat = ''

    response = req.content.decode('utf8')
    if response.find('<strong>Strictly Necessary</strong>') != -1:
        lbl_cat = "Strictly Necessary"
    if response.find('<strong>Targeting/Advertising</strong>') != -1:
        lbl_cat = "Targeting/Advertising"
    if response.find('<strong>Unknown</strong>') != -1:
        lbl_cat = "Unknown"
    if response.find('<strong>Functionality</strong>') != -1:
        lbl_cat = "Functionality"
    if response.find('<strong>Performance</strong>') != -1:
        lbl_cat = "Performance"
    return lbl_cat

    """
    cat = re.search(
        "The main purpose of this cookie is: <strong>([a-zA-Z]*( [a-zA-Z]*)*)</strong>", response)
    print(cat)
    if cat:
        return cat.group(1)
    else:
        return ''
    """


def pushRows(p_tableID, p_rows, p_timeout=60):
    table_id = p_tableID

    try:
        errors = client.insert_rows_json(table_id, p_rows, timeout=p_timeout)
        if errors == []:
            print('pushed rows to BigQuery:' +
                  p_tableID + ': ' + str(len(p_rows)))
        else:
            raise Exception(
                p_tableID + ": Encountered errors while inserting rows: {}".format(errors))
    except:
        print('error while pushing.. retry..')
        errors = client.insert_rows_json(table_id, p_rows, timeout=30)
        if errors == []:
            print('pushed rows to BigQuery:' +
                  p_tableID + ': ' + str(len(p_rows)))
        else:
            raise Exception(
                p_tableID + ": Encountered errors while inserting rows: {}".format(errors))


if __name__ == "__main__":
    start()
   # print(getCat('MUID'))
