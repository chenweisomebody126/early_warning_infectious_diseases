import scrapy

class ALLAFRICA_Spider(scrapy.Spider):
    name = 'allafrica'

    #allowed_domains= ["www.who.int/entity/mediacentre/news/releases"]
    allowed_domains= ["allafrica.com"]
    start_urls = ['http://allafrica.com/misc/sitemap/topics.html']

    def parse(self, response):
        # follow individual topic links
        for topic in response.xpath('(//div[@class ="category-grid"])[1]/ul/li/a/@href').extract():
            if topic is not None:
                topic =response.urljoin(topic+"?page=1")
                yield scrapy.Request(topic, callback=self.parse_topic_archive)


    def parse_topic_archive(self, response):
        top_news =response.xpath('//div["section top-news"]')
        if top_news:
            # follow links to news content pages
            for href in top_news.xpath('.//ul[@class="stories"]/li/a/@href').extract():
                 yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

            # follow pagination links
            for next_page in top_news.xpath('.//div[@class="pagination"]//ul/li/a/@href').extract():
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_topic_archive)


    def parse_news(self, response):
        title = response.css('div.heading h1.headline::text').extract_first()
        content_list = response.xpath('//div[@class="story-body"]/p[@class="story-body-text"]//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8')
        filename = '%s.txt' % str(title).strip().replace('/',"-")
        print ''.join(content)
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)
