# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class LianjiaItem(Item):
	region=Field()
	href=Field()
	name=Field()
	style=Field()
	area=Field()
	orientation=Field()
	decoration=Field()
	elevator=Field()
	floor=Field()
	build_year=Field()
	sign_time=Field()
	unit_price=Field()
	total_price=Field()
	fangchan_class=Field()
	school=Field()
	subway=Field()
#class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass
