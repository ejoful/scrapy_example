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
    img_url = scrapy.Field()

    # 进入页面后
    des = scrapy.Field()
    qq = scrapy.Field()
    teacher_name = scrapy.Field()
    teacher_link = scrapy.Field()
    teacher_des = scrapy.Field()


    course = scrapy.Field()
#
# class Chapter(scrapy.item):
#     title = scrapy.Field()
#     link = scrapy.Field()
#     time = scrapy.Field()
#
#     # 进入视频界面
#     video_link = scrapy.Field()











