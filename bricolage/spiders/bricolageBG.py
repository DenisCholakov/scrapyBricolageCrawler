import scrapy
import re
from bricolage.items import BricolageItem
from itemloaders import ItemLoader



class BricolagebgSpider(scrapy.Spider):
    name = 'bricolageBG'
    allowed_domains = ['mr-bricolage.bg']
    start_urls = ['https://mr-bricolage.bg/instrumenti/elektroprenosimi-instrumenti/vintoverti/c/006003013']

    def parse(self, response): 
        products = response.css('.product')
        for product in products:
            product_link = product.css('.image a::attr(href)').get()

            if product_link is not None:
                yield response.follow(product_link, callback=self.take_product)

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def take_product(self, response):
        # token = self.getToken(response)
        # productCode = re.search(r'[0-9]+', response.css('.bricolage-code::text').get())[0]
        l = ItemLoader(item = BricolageItem(), selector=response)

        l.add_css('name', 'h1::text')
        l.add_css('price', 'p.price::text')
        l.add_css('pictures', '.owl-thumbs img::attr(src)')

        fields = response.css('.product-classifications tbody tr')
        characteristics = {};

        for field in fields:
            values = field.css('td::text').getall()
            characteristics[values[0].strip()] = self.cleartext(values[1])

        l.add_value('characteristics', characteristics)

        # get_stores_body = f'locationQuery=&cartPage=false&entryNumber=0&latitude=42.6641056&longitude=23.3233149&CSRFToken={token}'

        # if productCode is not None:
        #     yield response.follow(
        #         f'https://mr-bricolage.bg/store-pickup/{productCode}/pointOfServices', 
        #         method = 'POST', body = get_stores_body,
        #         meta = {'l': l.load_item()},
        #         callback = self.getStores())

        yield l.load_item()

    # def getStores(self, response):
        

    def cleartext(self, value):
        value = re.sub(r'\t|\n|\xa0', '', value)
        return value.strip()

    def getToken(self, response):
        return re.match(r"CSRFToken = \'([-\w]+\w+)\'", response)[0]
