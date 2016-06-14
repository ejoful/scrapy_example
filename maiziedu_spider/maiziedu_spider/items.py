# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaizieduSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分页界面
    course_title = scrapy.Field()
    course_link = scrapy.Field()
    course_img = scrapy.Field()

    # 进入页面后
    course_des = scrapy.Field()
    course_qq = scrapy.Field()
    course_teacher_name = scrapy.Field()
    course_teacher_img = scrapy.Field()
    course_teacher_des = scrapy.Field()

    title = scrapy.Field()
    link = scrapy.Field()
    time = scrapy.Field()

    # 进入视频界面
    video_link = scrapy.Field()










