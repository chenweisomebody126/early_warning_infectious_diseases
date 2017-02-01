import scrapy

class WHOSpider(scrapy.Spider):
    name = 'who'

    #allowed_domains= ["www.who.int/entity/mediacentre/news/releases"]
    allowed_domains= ["www.who.int"]
    start_urls = ['http://www.who.int/mediacentre/news/releases/previous/en/']

    def parse(self, response):
        # follow links to news content pages
        for href in response.css('ul.auto_archive li a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

        # follow pagination links
        for next_page in response.css('div.paging li a::attr(href)').extract():
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_news(self, response):
        title = response.xpath('//div[@id="primary"]/h1[@class="headline"]/text()').extract_first()
        content_list = response.xpath('//div[@id="primary"]//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8')
        filename = '%s.txt' % str(title).strip().replace('/',"-")
        #print ''.join(content)
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)

        '''
        def extract_with_css():
            for i in response.xpath('//div[@id="primary"]')[0]:
                content+=i.xpath('.//text()')

                #for s in i.xpath('.//script | .//style | .//figure'):
                for s in i.xpath('.//h1/text() | .//h3/text() | .//p/text()').extract():
                    if s
                    s.append('\n')

            for i in bsObj.find('div',{"id":"primary"}).find_all(recursive=False):
    			for s in i.find_all(["script","style","figure"]):
    				s.extract()
    			for s in i.find_all("h3"):
    				s.append('\n')
    			content+=i.get_text()

            return content
        '''
