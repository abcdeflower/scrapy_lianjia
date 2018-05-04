from scrapy import Spider,Request
import re
from lxml import etree
import json
from urllib.parse import quote
from lianjia.items import LianjiaItem
import re


class Lianjia_spider(Spider):
	name='lianjia'
	regions={
	'daxing':'大兴',
	'yizhuangkaifaqu':'亦庄开发区',
	'yizhuang1':'亦庄',
	'shunyi':'顺义',
	'xihongmen':'西红门'
	}

	def start_requests(self):
		for region in list(self.regions.keys()):
			url="https://bj.lianjia.com/ershoufang/"+region+"/"
			yield Request(url=url,callback=self.parse,meta={'region':region})

	def parse(self,response):
		region=response.meta['region']
		selector=etree.HTML(response.text)
		sel=selector.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0]
		print(region,'页数：',sel,'|',type(sel))
		sel=json.loads(sel)
		total_pages=sel.get('totalPage')

		for i in range(int(total_pages)):
			url_page="https://bj.lianjia.com/ershoufang/{}/pg{}/".format(region,str(i+1))
			yield Request(url=url_page,callback=self.parse_ershoufang,meta={'region':region})

	def parse_ershoufang(self,response):
		region=response.meta['region']
		print('进入二级访问。。。')
		urls=response.xpath('//li[@class="clear"]/div[@class="info clear"]/div[@class="title"]/a/@href').extract()
		#print('获取页面url:',urls)
		for url in urls:
			#print('连接：',url)
			yield Request(url=url,callback=self.parse_end,meta={'region':region,'url':url})

	def parse_end(self,response):
		
		region=response.meta['region']
		href=response.meta['url']
		name=response.xpath('//div[@class="content"]/div[@class="title"]/h1/text()').extract()
		messages=response.xpath('//div[@class="content"]/ul/li/text()').extract()
		print('基本属性：',messages)
		style=messages[1]
		orientation=messages[6]
		decoration=messages[8]
		elevator=messages[11]
		floor=messages[1]
		sign_time=''
		fangchan_class=messages[13]
		school=''
		subway=response.xpath('//div[@class="introContent showbasemore"]/div[4]/div[2]/text()').extract()
	
		if isinstance(subway,list) and len(subway)>0:
			subway=subway[0]
			subway=re.sub('\n+','',subway[0])
			subway=re.sub(' +',' ',subway)
		else:
			subway=''
					
		
	
		#total_price=response.xpath('//div[@class="price"]/span[@class="total"]/text()').extract()#+response.xpath('//div[@class="price"]/span[@class="unit"]/span/text()').extract()[0]
		total_price=response.xpath('//body/div[5]/div[2]/div[2]/span[1]/text()').extract()
		print('总价：',total_price)
		unit_price=response.xpath('//div[@class="unitPrice"]/span/text()').extract()
		build_year=response.xpath('//div[@class="subInfo"]/text()').extract()
		area=response.xpath('//div[@class="aroundInfo"]/div[@class="communityName"]/a[@class="info"]/text()').extract()

		item=LianjiaItem()
		item['region']=region
		item['href']=href
		item['name']=name
		item['style']=style
		item['orientation']=orientation
		item['decoration']=decoration
		item['elevator']=elevator
		item['floor']=floor
		item['sign_time']=sign_time
		item['fangchan_class']=fangchan_class
		item['school']=school
		item['subway']=subway
		item['total_price']=total_price
		item['unit_price']=unit_price
		item['build_year']=build_year
		item['area']=area

		yield item



