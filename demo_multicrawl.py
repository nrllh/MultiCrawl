
from CrawlerOpenWPM_Wrapper import initiliaze_openwpm
from Objects import QueueItem
from CrawlerOpenWPM import runOpenWPMInstance
from CrawlerOpenWPM import CrawlerOpenWPM

q_item=QueueItem('https://internet-sicherheit.de','https://internet-sicherheit.de', 'waiting', None,None,None,None)

#initiliaze_openwpm(None, q_item) # only crawls
c=CrawlerOpenWPM()


c.runOpenWPMInstance(None, q_item) # crawl + push to BQ
