# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ChainItem(Item):
    Product_Name = Field()
    Order_Guide_Line_No = Field()
    Product_Code = Field()
    UPC_Code = Field()
    Category = Field()
    Unit_Of_Measure = Field()
    Case_Weight = Field()
    Case_Size_WxHxD = Field()
    Unit_Weight = Field()
    Unit_Size_WxHxD = Field()
    Pallet_Qty = Field()
    Country_Of_Origin = Field()
    Availability = Field()
    Unit_Price = Field()
    Image_link = Field()