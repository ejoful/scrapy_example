# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonItemExporter

from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
import urlparse
from os.path import basename
from urllib import quote, unquote


class MaizieduSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.first_item = True



    def process_item(self, item, spider):
        if self.first_item:
            self.first_item = False
            file = open('%s_items.json' % spider.name, 'wb')
            # scrapy 使用item export输出中文到json文件，内容为unicode码，如何输出为中文？
            # http://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
            # 里面有提到，将 JSONEncoder 的 ensure_ascii 参数设为 False 即可。
            # 因此就在调用 scrapy.contrib.exporter.JsonItemExporter 的时候额外指定 ensure_ascii=False 就可以啦。
            self.exporter = JsonItemExporter(file, ensure_ascii=False)
            self.exporter.start_exporting()
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):

    def __init__(self):

        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db='maiziedu_new',
            host='127.0.0.1',
            user='root',
            passwd='',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=True)



    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create recode if doesn't exist.
        # all this block run on it's own thread

        # tx.execute("select * from `tbl_course` where id = %s", (item['id']))
        # result = tx.fetchone()
        # if result:
        #     log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        # else:
            sql = """INSERT INTO `tbl_course` (`id`, `title`, `des`, `img`, `teacher_id`,`keywords`)
                    VALUES (%s,%s,%s,%s,%s,%s)"""
            lis = (item['id'], item['title'], item['des'], item['img'], item['teacher_id'], item['keywords'])
            tx.execute(sql, lis)

            for index, le in enumerate(item['lessons']):
                lesson = (le['video_id'], item['id'], le['title'], le['link'], le['video_link'], index+1)
                sql = """INSERT INTO `tbl_video` (`id`, `course_id`, `title`, `link`, `video_link`, `position`)
                                             VALUES (%s,%s,%s,%s,%s,%s)"""
                tx.execute(sql, lesson)





    def handle_error(self, e):
        print ('handle_error')
        log.err(e)


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        image_guid = urlparse.unquote(image_guid).decode('utf-8')
        return '%s' % (image_guid)
