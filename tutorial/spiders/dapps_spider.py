import scrapy
import re


class DappsSpider(scrapy.Spider):
    name = "dapps"
    start_urls = [
        'https://www.stateofthedapps.com/rankings/platform/ethereum',
        'https://www.stateofthedapps.com/rankings/platform/eos',
        'https://www.stateofthedapps.com/rankings/platform/gochain',
        'https://www.stateofthedapps.com/rankings/platform/poa',
        'https://www.stateofthedapps.com/rankings/platform/steem',
        'https://www.stateofthedapps.com/rankings/platform/xdai',
        'https://www.stateofthedapps.com/rankings/platform/loom'
    ]

    def parse(self, response):
        parser = self.parser(response)
        for result in parser.parse():
            yield result

    class parser():
        def __init__(self, response):
            self.current_page = 1
            self.pages_number = self.get_pages_number(
                response.css('span.button-inner::text').getall())
            self.url = response.url
            self.platform = re.findall(r'/[a-zA-Z]*', self.url)[-1][1:]
            self.response = response

        def parse(self, response=None):
            if response == None:
                response = self.response
            # Follow links to app pages
            for href in response.css('h4.name a::attr(href)'):
                yield response.follow(href, self.parse_dapp)

            if self.current_page + 1 <= self.pages_number:
                self.current_page = self.current_page + 1
                next_page = self.url + \
                    '?page=' + str(self.current_page + 1)
                yield response.follow(next_page, callback=self.parse)

        def parse_dapp(self, response):
                # Still need to format the strength and rank
            yield {
                'platform': self.platform,
                'name': response.css('div.DappDetailBodyHeading h1 span::text').get(),
                'shortdesc': response.css('div.DappDetailBodyHeading span.heading-tagline::text').get(),
                'image-src': response.css('div.DappDetailBodyContent div.wrapper-inner div.DappDetailBodyContentImage img::attr(src)').get(),
                'desc': response.css('div.DappDetailBodyContent div.wrapper-inner div.DappDetailBodyContentDescription p::text').get(),
                'status': response.css('div.DappDetailBodyContentModulesStatus strong::text').get(),
                'author': self.authors_filter(response.css('div.DappDetailBodyContentModulesAuthors span::text').getall()),
                'license': response.css('div.DappDetailBodyContentModulesLicense p::text').get(),
                'lastupdated': response.css('div.DappDetailBodyContentModulesUpdated strong::text').get(),
                'submitted': response.css('div.DappDetailBodyContentModulesSubmitted strong::text').get(),
                'devevents_30d': self.try_get(lambda: response.css('p.dev-data::text')[0].get()),
                'deveventsincrease': self.try_get(lambda: response.css('p.dev-data')[0].css('span::text').getall()[2]),
                'devevents_90d': self.try_get(lambda: response.css('p.dev-data::text')[2].get()),
                'activeusers_daily': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[0].css('li')[0].css('span.stat-value::text').get()),
                'activeusers_weekly': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[0].css('li')[1].css('span.stat-value::text').get()),
                'activeusers_monthly': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[0].css('li')[2].css('span.stat-value::text').get()),
                'tx_1d': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[1].css('li')[0].css('span.stat-value::text').get()),
                'tx_7d': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[1].css('li')[1].css('span.stat-value::text').get()),
                'tx_30d': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[1].css('li')[2].css('span.stat-value::text').get()),
                'volume_1d': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[2].css('li')[0].css('span.stat-value::text').get()),
                'volume_7d': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[2].css('li')[1].css('span.stat-value::text').get()),
                'volume_30d': self.try_get(lambda: response.css('div.DappDetailBodyContentModulesStats')[2].css('li')[2].css('span.stat-value::text').get()),
                'icon-src': response.css('h1.heading-title img::attr(src)').get(),
                'mainnet_contracts': self.try_get(lambda: response.css('li.DappDetailBodyContentModulesContractsItem')[0].css('a::attr(href)').getall()),
                'ropsten_contract': self.try_get(lambda: response.css('li.DappDetailBodyContentModulesContractsItem')[1].css('a::attr(href)').getall()),
                'category': response.css('li.category-item a::text').get(),
                'tags': response.css('li.tag-item a::text').getall(),
                'profile_strength': response.css('div.DappProfile p::text').get(),
                'rank': response.css('div.DappDetailBodyContentRank p::text').get(),
                'recommend': response.css('li.reaction-item span::text').getall(),
                'socialnets': response.css('li.social-item a::attr(href)').getall(),
                'review_title': response.css('li.review-item h4.title a::text').getall(),
                'review_author': response.css('p.author-date strong::text').getall(),
                'review_date': response.css('p.author-date::text').getall(),
                'review_summary': response.css('p.summary::text').getall(),
                'website': response.url
            }

        def try_get(self, exec):
            try:
                return exec()
            except IndexError:
                return None

        def authors_filter(self, authors):
            res = []
            for author in authors:
                author = re.search(r'[a-zA-Z\s]*', author).group()
                if len(author) != 0:
                    res.append(author)
            return res

        def get_pages_number(self, button_numbers):
            def to_number(s):
                try:
                    return int(s)
                except ValueError:
                    return 0
            return max(map(to_number, button_numbers))
