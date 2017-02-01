import scrapy

class REUTERWORLDSpider(scrapy.Spider):
    name = 'reuterworld'

    #allowed_domains= ["www.who.int/entity/mediacentre/news/releases"]
    allowed_domains= ["reuters.com"]
    start_urls = ['http://www.reuters.com/news/archive/worldNews?view=page&page=1&pageSize=10']

    def parse(self, response):
        # follow links to news content pages
        for href in response.xpath('//div[@class="news-headline-list "]//h3[@class="story-title"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

        # follow pagination links
        for next_page in response.xpath('//div[@class="module"]//a[@class="control-nav-next"]/@href').extract():
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.xpath('//h1[@class="article-headline"]/text()').extract_first()
        content_list = response.xpath('//span[@id="article-text"]//p//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8')
        filename = '%s.txt' % str(title).strip()
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)
