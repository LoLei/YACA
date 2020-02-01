# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item


class PageItem(Item):
    url = Field()
    parent_url = Field()
    content_type = Field()
    status = Field()
    title = Field()
    h1 = Field()
    children = Field()
    ahrefs = Field()
