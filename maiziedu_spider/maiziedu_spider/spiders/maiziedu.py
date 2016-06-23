# -*- coding: utf-8 -*-
import scrapy
from maiziedu_spider.items import Course
# from maiziedu_spider.items import Chapter


class MaizieduSpider(scrapy.Spider):
    name = "maiziedu"
    allowed_domains = ["maiziedu.com"]
    start_urls = (
        'http://www.maiziedu.com',
    )

    def start_requests(self):
        reqs = []
        for i in range(1,37):
            req = scrapy.Request("http://www.maiziedu.com/course/list/all-all/0-%s/"%i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        course_list = response.xpath("//ul[@class='zy_course_list']")

        trs = course_list[0].xpath('li')

        for course in trs[0:]:
            course_item = Course()

            course_item['title'] = course.xpath('a/@title')[0].extract()

            course_item['link'] = ["http://www.maiziedu.com" + course.xpath('a/@href')[0].extract()]

            course_item['img_url'] = ["http://www.maiziedu.com" + course.xpath('a/p/img/@src')[0].extract()]

            yield scrapy.Request(url=course_item['link'][0], meta={'course_item': course_item}, callback=self.parse_detail,
                             dont_filter=True)

    def parse_detail(self, response):
        course_item = response.meta['course_item']

        course_item['des'] = response.xpath('//p[@class="color66 font14 marginB10 p2"]/text()')[0].extract()

        course_item['qq'] = response.xpath('//p[@class="lv_btn"]/a[@class="a2 color66 VLCico"]/text()')[0].extract()

        course_item['teacher_name'] = response.xpath('//div[@class="teacher-info marginB20"]/div/h3/text()')[0].extract()

        course_item['teacher_link'] = ["http://www.maiziedu.com" + response.xpath('//div[@class="teacher-info marginB20"]/a/@href')[0].extract()]

        course_item['teacher_des'] = response.xpath('//div[@class="teacher-info marginB20"]/p/text()')[0].extract()

        lesson_lists = response.xpath("//ul[@class='lesson-lists']")

        lesson = lesson_lists[0].xpath('li')

        for les in lesson[0:]:
            title = les.xpath('a/span/text()')[0].extract()

            link = ["http://www.maiziedu.com" + les.xpath('a/@href')[0].extract()][0]


            yield scrapy.Request(url=link, meta={'course_item': course_item,'title':title,'link':link}, callback=self.parse_video,
                             dont_filter=True)


    def parse_video(self, response):
        course_item = response.meta['course_item']
        title = response.meta['title']
        link = response.meta['link']

        video_link = response.xpath('//source/@src')[0].extract()

        course_item['course'] = {'title':title,'link':link,'video_link':video_link}

        yield course_item
    #     chapter_list = response.xpath("//ul[@class='lesson-lists']")
    #
    #     chapters = chapter_list[0].xpath['li']
    #
    #     for ch in chapters[0:]:
    #         chapter_item = Chapter()
    #
    #         chapter_item['title'] = ch.xpath("a/span[@class='f1']")[0].extract()
    #
    #         chapter_item['link'] = response.urljoin(ch.xpath("a/span[@class='f1']")[0].extract())
    #
    #         chapter_item['time'] = ch.xpath("a/span[@class='f1']")[0].extract()
    #
    #         yield scrapy.Request(url=chapter_item['link'], meta={'chapter_item': chapter_item}, callback=self.parse_video,
    #                          dont_filter=True)
    #
    # def parse_video(self, response):
    #     chapter_item = response.meta['chapter_item']
    #
    #     chapter_item['video_link'] = response.xpath('//*[@id="microohvideo_html5_api"]/source::attr(src)')
    #
    #     yield chapter_item




