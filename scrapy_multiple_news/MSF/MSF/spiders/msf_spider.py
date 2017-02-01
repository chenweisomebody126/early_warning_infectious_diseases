import scrapy

class MSFSpider(scrapy.Spider):
    name = 'msf'

    #allowed_domains= ["www.who.int/entity/mediacentre/news/releases"]
    allowed_domains= ["doctorswithoutborders.org"]
    start_urls = ['http://www.doctorswithoutborders.org/news-stories/press/press-releases']

    def parse(self, response):
        # follow links to news content pages
        for href in response.xpath('//div[@class="view-content"]//div[@class="field-items"]//h3/a/@href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

        # follow pagination links
        for next_page in response.xpath('//ul[@class="pager"]/li/a/@href').extract():
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.xpath('//h1[@class="title" and @id="page-title"]/text()').extract_first()
        content_list = response.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]//p//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8')
        filename = '%s.txt' % str(title).strip().replace('/',"-")
        #print ''.join(content)
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)
