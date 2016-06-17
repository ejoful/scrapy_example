# -*- coding: utf-8 -*-
import scrapy
from maiziedu_spider.items import Course,Chapter,Teacher


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

        for course in trs[0:]:
            course_item = Course()

            course_item['title'] = course.xpath('a::attr(title)')

            course_item['link'] = course.xpath('a::attr(href)')

            course_item['img'] = course.xpath('a/p/img::attr(src)')

            yield scrapy.Request(url=item["GOODS_URL"], meta={'item': item}, callback=self.parse_detail,
                             dont_filter=True)
