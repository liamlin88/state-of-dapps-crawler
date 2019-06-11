import scrapy

class FeaturesSpider(scrapy.Spider):
    name = "features"
    start_urls = [
        'https://www.stateofthedapps.com/collections/featured',
    ]

    def parse(self, response):
        for name in response.css('h4.title-4::text').getall():
            yield {
                'name' : name
            }