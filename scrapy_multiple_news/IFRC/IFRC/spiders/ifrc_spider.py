import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import time

class IFRCSpider(scrapy.Spider):
    name = 'ifrc'

    allowed_domains= ["ifrc.org"]
    start_urls = ['http://www.ifrc.org/en/news-and-media/press-releases/']
    def __init__(self):
        self.browser = webdriver.Chrome('/Users/macbook/Downloads/chromedriver')

    def parse(self, response):
        self.browser.get(response.url)
        while True:
            next_page = self.browser.find_element_by_xpath('//div[@class="PagingContainer"]/a[@title="Next Page"]')
            try:
                next_page.click()
                time.sleep(2)
                source = self.browser.page_source
                #pass into scrapy.Selector to extract news content page
                sel = Selector(text=source)
                for href in sel.xpath('//div[@class="cw_newsgroup"]//a/@href').extract():
                    #print "href", href
                    yield scrapy.Request(response.urljoin(href), callback=self.parse_news)
            except:
                break

        self.browser.close()

    def parse_news(self, response):
        title = response.xpath('//div[@class="cw_headbox cw_titelgroupmiddle"]//h1/text()').extract_first()
        content_list = response.xpath('//div[@id="cw_content" and @class="container-fluid"]//p//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8')
        filename = '%s.txt' % str(title).strip().replace('/',"-")
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)
