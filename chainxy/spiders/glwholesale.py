import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import html
import pdb

class glwholesaleSpider(scrapy.Spider):
	name = 'glwholesale'
	domain = 'http://www.glwholesale.com'

	def start_requests(self):
		yield scrapy.Request(url=self.domain, callback=self.parse_category)
		
	def parse_category(self, response):
		category_list = response.xpath('//ul[@class="dropdown-menu"]//a/@href').extract()
		for category in category_list:
			for cnt in range(1, 20):
				category_url = self.domain + category + '?page=' + str(cnt)
				yield scrapy.Request(url=category_url, callback=self.parse_product)
		
	def parse_product(self, response):
		try:
			product_list = response.xpath('//div[contains(@class, "product-thumb")]//a/@href').extract()
			for product in product_list:
				if 'product' in product:
					product = self.domain + product
					yield scrapy.Request(url=product, callback=self.parse_page)
		except:
			pass

	def parse_page(self, response):
		try:
			item = ChainItem()
			item['Product_Name'] = self.validate(response.xpath('//h2[@class="product-description"]/text()').extract_first())
			detail = self.eliminate_space(response.xpath('//dl[contains(@class, "product-details")]//text()').extract())
			for cnt in range(0, len(detail)):
				if detail[cnt] == 'Order Guide Line No':
					item['Order_Guide_Line_No'] = detail[cnt+1]
				if detail[cnt] == 'Product Code':
					item['Product_Code'] = detail[cnt+1]
				if detail[cnt] == 'UPC Code':
					item['UPC_Code'] = detail[cnt+1]
				if detail[cnt] == 'Category':
					item['Category'] = detail[cnt+1]
				if detail[cnt] == 'Unit of Measure':
					item['Unit_Of_Measure'] = detail[cnt+1]
				if detail[cnt] == 'Case Weight':
					item['Case_Weight'] = detail[cnt+1]
				if detail[cnt] == 'Case Size (WxHxD)':
					item['Case_Size_WxHxD'] = detail[cnt+1]
				if detail[cnt] == 'Unit Weight':
					item['Unit_Weight'] = detail[cnt+1]
				if detail[cnt] == 'Unit Size (WxHxD)':
					item['Unit_Size_WxHxD'] = detail[cnt+1]
				if detail[cnt] == 'Pallet Qty':
					item['Pallet_Qty'] = detail[cnt+1]
				if detail[cnt] == 'Country of Origin :':
					item['Country_Of_Origin'] = detail[cnt+1]
				if detail[cnt] == 'Availability':
					item['Availability'] = detail[cnt+1]
				if detail[cnt] == 'Unit Price':
					item['Unit_Price'] = detail[cnt+1]
			img_list = self.eliminate_space(response.xpath('//div[@class="container"]//img/@src').extract())
			item['Image_link'] = img_list[2]
			yield item
		except:
			pass

	def validate(self, item):
		try:
			return item.strip()
		except:
			return ''

	def eliminate_space(self, items):
		tmp = []
		for item in items:
			if self.validate(item) != '':
				if self.validate(item) == '-----' or 'login' in self.validate(item).lower():
					tmp.append('')
				else:
					tmp.append(self.validate(item))
		return tmp
