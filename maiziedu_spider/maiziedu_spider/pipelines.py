# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonItemExporter

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





