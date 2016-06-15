# -*- coding: utf-8 -*-
import scrapy
from maiziedu_spider.items import MaizieduSpiderItem


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
        course_list = response.xpath("//ul[@class='zy_course_list']")

        trs = course_list[0].xpath['li']

        items = []

        for course in trs[0:]:
            pre_item = MaizieduSpiderItem()

            pre_item['course_title'] = course.xpath('a::attr(title)')

            pre_item['course_link'] = course.xpath('a::attr(href)')

            pre_item['course_img'] = course.xpath('a/p/img::attr(src)')

            items.append(pre_item)

        return items
