import scrapy
from frawler.items import BeerItem

class BestOfBeersSpider(scrapy.Spider):
    name = 'FeerSpider'
    start_urls = ['http://www.bestofbeers.dk/category/alle-oel-653/']
    allowed_domains = ["bestofbeers.dk"]
    download_delay=10.0

    def parse(self, response):
        for url in response.css('.pager li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        for product in response.css('.product'):
            beer = BeerItem()
            beer['title'] = product.css('.productInfo .productDesc .productHeader::text').extract()
            beer['price'] = product.css('.productInfo .productPrice .first::text').extract()
            if beer['title'] and beer['price']:
                yield beer
