from ap_web_crawler import *
from cidrap_web_crawler import *
#pip install pymysql
import pymysql
from login import *

def main():
    path= 'ncfpd.ahc.umn.edu\ncfpd\NCFPD\Erin\Web Scraping Files'

    web_crawler_list= [AP_WEB_CRAWLER(path), CIDRAP_WEB_CRAWLER(path)]
    #conn = cx_Oracle.connect(chen4626/135914UMNumn/@fpdi-tools-db.ahc.umn.edu/web_crawler_db)
    #conn = pymysql.connect(host='localhost',user='root',password='web_crawler',db='web_crawler_db',charset='utf8')
    conn = pymysql.connect(host=db_hostname,user=db_username,password=db_password,db=db_name,charset='utf8')
    cur =conn.cursor()

    # create table if one does not exist
    cur.execute("CREATE TABLE IF NOT EXISTS web_crawler_log_tb (title VARCHAR(255), pubDate DATE,link TEXT)")

    for web_crawler in web_crawler_list:
        #use itemGenerator to yield one item per time
        itemGenerator =web_crawler.fromRSSgetFeeds()
        for item in itemGenerator:
            title= item.title
            link=item.link
            #check we have scraped it already
            if web_crawler.if_exist_in_log_database(title,cur):
                print "skip %s" %title
            else:
                #from page URL within the feed to get the page content
                print title,"not existence"
                content= web_crawler.fromPageURLgetContent(link)
                if content:
                    #save content into filesystem
                    web_crawler.save_content_into_filesystem(title, content)
                    #log feed into log database
                    web_crawler.log_scraped_news_into_database(cur,title, link)
                    print "successfully saved feed %s" %item.title
    cur.close()
    conn.close()

if __name__== "__main__":
    main()
