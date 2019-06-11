import scrapy
import json

class MainpagePromoteSpider(scrapy.Spider):
    name = "mainpage_promote"
    start_urls = [
        'https://api.stateofthedapps.com/promoted/dapps',
    ]

    def parse(self, response):
        items = json.loads(response.body_as_unicode())
        for item in items:
            yield {
                'name': item['name']
            }
