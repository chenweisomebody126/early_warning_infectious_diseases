import pymysql
import feedparser
from urllib2 import Request, urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup

class CIDRAP_WEB_CRAWLER(object):
    def __init__(self, path):
        cidrap_all= "http://www.cidrap.umn.edu/news/all/rss"
        self.rss_link_list=[cidrap_all]
        self.path= path

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
            bsObj = BeautifulSoup(html,"lxml")
            content=""
            #print bsObj
            for i in bsObj.find('div',{"class":"field field-name-field-body field-type-text-long field-label-hidden"}).find_all(["p","h3"]):
             #we need to discriminate two situations
             #First is html link<a> is embedded in the <strong> along with paragragh we want to keep
             #Fortunately <a> is a child of <strong> from which we can identify and remove <a>
                for s in i.find_all("strong"):
                    s.extract()
            #second is html link <a> is exposed to <p> and we need to skip both words and link
                if i.find("a"):
                    continue
                else:
                    content+=i.get_text()
            return content
        except:
            print "AttributeError"
            return None


    def save_content_into_filesystem(self, title, content):
        #print "title",title
        with open(self.path+title.replace('/','-')+".txt", "w") as f:
            f.write(content.encode('utf8'))

    def log_scraped_news_into_database(self,cur, title, link):
        cur.execute("INSERT INTO web_crawler_log_tb (title, pubDate,link) VALUES (%s, DATE(NOW()), %s)", (title,link))
        #SQL instruction will not be executed until you "commit" it
        cur.connection.commit()
