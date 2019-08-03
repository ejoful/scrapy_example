# -*- coding: utf-8 -*-
import scrapy
from maiziedu_spider.items import Course
import sys
# from maiziedu_spider.items import Chapter


class MaizieduSpider(scrapy.Spider):
    name = "maiziedu"
    allowed_domains = ["maiziedu.com"]
    start_urls = (
        'http://www.maiziedu.com',
    )
    # 编码设置为utf8,避免中文显示为unicode编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def start_requests(self):
        reqs = []
        for i in range(1, 47):
            req = scrapy.Request("http://www.maiziedu.com/course/all-all/0-%s/" % i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        course_list = response.xpath("//ul[@class='course-lists']")

        trs = course_list[0].xpath('li')

        for course in trs[0:]:
            course_item = Course()

            url = course.xpath('a/@href')[0].extract()
            course_item['id'] = (url.split('/'))[-2]

            course_item['title'] = course.xpath('a/@title')[0].extract()

            course_item['link'] = ["http://www.maiziedu.com" + course.xpath('a/@href')[0].extract()]

            course_item['img_url'] = ["http://www.maiziedu.com" + course.xpath('a/p/img/@src')[0].extract()]

            url = course.xpath('a/p/img/@src')[0].extract()

            course_item['img'] = (url.split('/'))[-1]

            yield scrapy.Request(url=course_item['link'][0], meta={'course_item': course_item}, callback=self.parse_detail,
                             dont_filter=True)

    def parse_detail(self, response):
        course_item = response.meta['course_item']

        course_item['des'] = response.xpath('//p[@class="color66 font14 marginB10 p2"]/text()')[0].extract()

        course_item['keywords'] = response.xpath("//meta[@name='keywords']/@content")[0].extract()

        course_item['qq'] = response.xpath('//div[@class="lv_btn"]/a[@class="a2 color66 VLCico"]/text()')[0].extract()

        course_item['teacher_name'] = response.xpath('//div[@class="teacher-info marginB20"]/div/h3/text()')[0].extract()

        course_item['teacher_link'] = ["http://www.maiziedu.com" + response.xpath('//div[@class="teacher-info marginB20"]/a/@href')[0].extract()]

        url = response.xpath('//div[@class="teacher-info marginB20"]/a/@href')[0].extract()
        course_item['teacher_id'] = (url.split('/'))[-2]

        course_item['teacher_des'] = response.xpath('//div[@class="teacher-info marginB20"]/p/text()')[0].extract()

        lesson_lists = response.xpath("//ul[@class='lesson-lists']")

        lesson = lesson_lists[0].xpath('li')

        course_item['lessons'] = []
        return self.recursive_parse_video(lesson, course_item)

    def recursive_parse_video(self, tbd, course_item):
        if not tbd:
            yield course_item
        else:
            les = tbd.pop(0)
            title = les.xpath('a/span/text()')[0].extract()
            link = ["http://www.maiziedu.com" + les.xpath('a/@href')[0].extract()][0]

            yield scrapy.Request(url=link, meta={'tbd':tbd,'course_item': course_item,'title':title,'link':link}, callback=self.parse_video,
                             dont_filter=True)


    def parse_video(self, response):
        course_item = response.meta['course_item']
        title = response.meta['title']
        link = response.meta['link']
        video_id = (((link.split('/'))[-2]).split('-'))[-1]

        video_link = response.xpath('//source/@src')[0].extract()

        course_item['lessons'].append({'video_id':video_id, 'title':title, 'link':link, 'video_link':video_link})
        tbd = response.meta['tbd']
        return self.recursive_parse_video(tbd, course_item)


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




