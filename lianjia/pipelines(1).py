# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LianjiaPipeline(object):
	def process_item(self, item, spider):
		print('存储信息：',item)
		with open('aa.txt','a') as f:
			f.write(str(item))
			f.write('\n************************************\n')
		return item
