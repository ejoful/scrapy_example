# -*- coding: utf-8 -*-
import scrapy


class MaizieduSpider(scrapy.Spider):
    name = "maiziedu"
    allowed_domains = ["maiziedu.com"]
    start_urls = (
        'http://www.maiziedu.com',
    )

    def start_requests(self):
        reqs = []
        for i in range(1,2):
            req = scrapy.Request("http://www.maiziedu.com/course/list/all-all/0-%s/"%i)
            reqs.append(req)
        return reqs


    def parse(self, response):

        pass
