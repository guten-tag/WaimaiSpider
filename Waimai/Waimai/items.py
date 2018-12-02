# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WaimaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    id = scrapy.Field()
    name = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    float_delivery_fee = scrapy.Field()
    float_minimum_order_amount = scrapy.Field()
    opening_hours = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    recent_order_num = scrapy.Field()
    flavors = scrapy.Field()


class RateItem(scrapy.Item):

	rate = scrapy.Field()
		

class TypeItem(scrapy.Item):

	MeiShi = scrapy.Field()
	KuaiCanBianDang = scrapy.Field()
	TeSeCaiXi = scrapy.Field()
	YiGuoLiaoLi = scrapy.Field()
	XiaoChiYeXiao = scrapy.Field()
	TianPinYinPin = scrapy.Field()
	GuoShuShengXian = scrapy.Field()
	ShangDianChaoShi = scrapy.Field()
	XianHuaLvZhi = scrapy.Field()
	YiYaoJianKang = scrapy.Field()
	ZaoCan = scrapy.Field()
	WuCan = scrapy.Field()
	XiaWuCha = scrapy.Field()
	WanCan = scrapy.Field()
	YeXiao = scrapy.Field()