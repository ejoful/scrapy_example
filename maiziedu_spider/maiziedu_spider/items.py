# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Course(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分页界面
    #
    title = scrapy.Field()
    link = scrapy.Field()
    img = scrapy.Field()

    # 进入页面后
    des = scrapy.Field()
    qq = scrapy.Field()
    teacher_id = scrapy.Field()


class Teacher(scrapy.item):
    name = scrapy.Field()
    img = scrapy.Field()
    des = scrapy.Field()


class Chapter(scrapy.item):
    title = scrapy.Field()
    link = scrapy.Field()
    time = scrapy.Field()

    # 进入视频界面
    video_link = scrapy.Field()











