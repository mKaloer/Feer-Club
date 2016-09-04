import re
import scrapy
from frawler.items import BeerItem

class BestOfBeersSpider(scrapy.Spider):
    name = 'FeerSpider'
    start_urls = ['http://www.bestofbeers.dk/category/alle-oel-653/']
    allowed_domains = ["bestofbeers.dk"]
    download_delay=10.0

    REAL_NMBR_REGEX = re.compile(".*?(\d+[\.|,]?\d*)")
    PERCENTAGE_REGEX = re.compile(".*?(\d+[\.|,]?\d*)\s*%")

    def parse(self, response):
        # All product pages
        for url in response.css('.pager li a::attr("href")').re('.*/category/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse)
        # For each specific beer
        for url in response.css('#catView .product a.productHeader::attr("href")').re('.*/product/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_product)

    def parse_product(self, response):
        beer = BeerItem()
        title = response.css('.sectionHeader h1::text').extract_first()
        BestOfBeersSpider.extract_info_from_title(title, beer)
        price_string = response.css('#productInfo #priceInfo .current.price span::text').extract_first()
        beer['price'] = BestOfBeersSpider.REAL_NMBR_REGEX.match(price_string).group(1).replace(',', '.')
        beer['brewery'] = response.css('#productInfo #productDetails #infolist .manufacture::text').extract_first()
        beer['purchase_url'] = response.url
        if beer['name'] and beer['price']:
            yield beer

    @staticmethod
    def extract_info_from_title(title, beer):
        beer['name'] = title.split(",")[0]
        abv_matches = BestOfBeersSpider.PERCENTAGE_REGEX.match(title).groups()
        if len(abv_matches) > 0:
            beer['abv'] = float(abv_matches[0].replace(",", "."))
        # TODO: style, name and volume
