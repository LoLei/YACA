# http://scrapingauthority.com/2016/09/19/scrapy-exporting-json-and-csv/
# https://stackoverflow.com/questions/39213095/scrapy-export-csv-without-specifying-in-cmd

# -*- coding: utf-8 -*-
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class YACAScraperPipelineJSON(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open('%s.json' % spider.name, 'w+b')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8',
                ensure_ascii=False, indent=2)
        self.exporter.fields_to_export = ["url", "status",
                "title", "h1", "children", "ahrefs"]
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class YACAScraperPipelineCSV(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open('%s.csv' % spider.name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = ["url", "parent_url", "content_type",
                "status", "title", "h1"]
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
