import scrapy

class RELIEFWEBSpider(scrapy.Spider):
    name = 'reliefweb'

    #allowed_domains= ["www.who.int/entity/mediacentre/news/releases"]
    allowed_domains= ["reliefweb.int"]
    start_urls = ['http://reliefweb.int/updates?format=8&disaster_type=4642&language=267#content']

    def parse(self, response):
        # follow links to news content pages
        for href in response.xpath('//div[@class="river-list river-updates"]/div[@class="item "]/div[@class="title"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

        # follow pagination links
        for next_page in response.xpath('//ul[@class="links pager pager-list"]/li/a/@href').extract():
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.xpath('//div[@class="region region-content"]//h1[@class="node-title clearfix"]/text()').extract_first()
        content_list = response.xpath('//div[@class="region region-content"]//div[@class="node-content clearfix"]//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8')
        filename = '%s.txt' % str(title).strip().replace('/',"-")
        #print ''.join(content)
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)
