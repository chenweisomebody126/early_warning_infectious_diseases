import pymysql
import feedparser
from urllib2 import Request, urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup

class AP_WEB_CRAWLER(object):
    def __init__(self, path):
        ap_top_news= "http://hosted.ap.org/lineups/TOPHEADS.rss?SITE=AP&SECTION=HOME"
        ap_US_national= "http://hosted.ap.org/lineups/USHEADS.rss?SITE=AP&SECTION=HOME"
        ap_world = "http://hosted.ap.org/lineups/WORLDHEADS.rss?SITE=AP&SECTION=HOME"
        ap_politics= "http://hosted.ap.org/lineups/POLITICSHEADS.rss?SITE=AP&SECTION=HOME"
        ap_washingtion = "http://hosted.ap.org/lineups/WASHINGTONHEADS.rss?SITE=AP&SECTION=HOME"
        ap_business ="http://hosted.ap.org/lineups/BUSINESSHEADS.rss?SITE=AP&SECTION=HOME"
        ap_tech = "http://hosted.ap.org/lineups/TECHHEADS.rss?SITE=AP&SECTION=HOME"
        ap_entertain= "http://hosted.ap.org/lineups/ENTERTAINMENT.rss?SITE=AP&SECTION=HOME"
        ap_health= "http://hosted.ap.org/lineups/HEALTHHEADS.rss?SITE=AP&SECTION=HOME"
        ap_science= "http://hosted.ap.org/lineups/SCIENCEHEADS.rss?SITE=AP&SECTION=HOME"


        self.rss_link_list=[ap_top_news,ap_US_national,ap_world,ap_politics, \
        ap_business, ap_tech, ap_entertain, ap_health, ap_science]
        self.path=path

    #first go to rss url and fetch page_url
    def fromRSSgetFeeds(self):
        for rss_link in self.rss_link_list:
            myfeed=feedparser.parse(rss_link)
            for item in myfeed.entries:
                yield item

    def if_exist_in_log_database(self, title, cur):
        # get connection and cursor upfront, before entering loop
        cur.execute("SELECT * FROM web_crawler_log_tb WHERE title = %s AND pubDate>= ( CURDATE() - INTERVAL 3 DAY )", (title))
        cur.connection.commit()
        if cur.rowcount==0:
            return False
        else: return True

    def fromPageURLgetContent(self, link):
        try:
        #modify the User-Agent in request to fool the server
            #req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            req = Request(link)
            html = urlopen(req).read()
        except:
            print "ExceptionError"
            return None
        try:
            bsObj = BeautifulSoup(html.decode('utf-8', 'ignore'),"lxml")
            content=""

            for paragragh in bsObj.find_all('p',{'class':"ap-story-p"}):
                if paragragh:
                    content+= paragragh.get_text()
            return content
        except:
            print "AttributeError"
            return None

    def save_content_into_filesystem(self, title, content):
        #path='/Users/macbook/Documents/RA/web_crawler_server/sample/'
        #print content
        with open(self.path+title+".txt", "w") as f:
            f.write(content.encode('utf8'))

    def log_scraped_news_into_database(self,cur, title, link):
        cur.execute("INSERT INTO web_crawler_log_tb (title, pubDate,link) VALUES (%s, DATE(NOW()), %s)", (title,link))
		#SQL instruction will not be executed until you "commit" it
        cur.connection.commit()
