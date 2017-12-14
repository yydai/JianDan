import scrapy

from scrapy.spiders import CrawlSpider, Rule
from photo_jiandan.items import PhotoJiandanItem
from scrapy.linkextractor import LinkExtractor
from scrapy.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
# use splash to execute js code
from scrapy_splash import SplashRequest


class PhotoSpider(CrawlSpider):
    name = 'jiandan'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/ooxx/page-1']

    def parse(self, response):
        # from page 1 to 320, you can change this
        for i in range(1, 320, 1):
            url = 'http://jandan.net/ooxx/page-{}'.format(i)
            yield SplashRequest(url, self.parse_item, args={'wait': 0.5})

    def parse_item(self, response):
        hxs = Selector(text=response.body)
        images = hxs.xpath(
            "//li[contains(@id,'comment')]/div/div/div[2]/p/img/@src").extract()
        items = []
        for image in images:
            item = PhotoJiandanItem()
            item['image_urls'] = [image]
            items.append(item)
        return items
