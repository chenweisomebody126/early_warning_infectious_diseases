import scrapy

class WHO_DO_Spider(scrapy.Spider):
    name = 'who_do'

    #allowed_domains= ["www.who.int/entity/mediacentre/news/releases"]
    allowed_domains= ["www.who.int"]
    start_urls = ['http://www.who.int/csr/don/archive/year/en/']

    def parse(self, response):
        # follow individual year links
        for year in response.css('div.col_2-1_1 li a::attr(href)').extract():
            if year is not None:
                year = response.urljoin(year)
                yield scrapy.Request(year, callback=self.parse_year_archive)

    def parse_year_archive(self, response):
        # follow links to news content pages
        for href in response.css('ul.auto_archive li a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_news)

    def parse_news(self, response):
        title = response.xpath('//div[@id="primary"]/h1[@class="headline"]/text()').extract_first()
        content_list = response.xpath('//div[@id="primary"]//text()').extract()
        content=""
        for i in content_list:
            content+=i.encode('utf8').strip()
        filename = '%s.txt' % str(title).strip().replace("/","-")
        #print ''.join(content)
        with open('./sample/'+filename, 'wb') as f:
            f.write(content)
            #f.write(''.join(content).encode('utf8'))
        self.log('Saved file %s' % filename)
