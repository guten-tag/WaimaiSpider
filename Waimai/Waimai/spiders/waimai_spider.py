# -*- encoding:utf-8 -*-

import scrapy
from scrapy.conf import settings
import json
import numpy
import re
import geohash2
from Waimai.items import WaimaiItem
from Waimai.items import RateItem
from Waimai.items import TypeItem

class WaimaiSpider(scrapy.Spider):

    name = "waimai"

    allowed_domains = ['ele.me']

    start_urls = [
            "https://www.ele.me/restapi/shopping/v2/restaurant/category?",
            "https://www.ele.me/restapi/shopping/restaurants?",
            "https://www.ele.me/restapi/ugc/v1/restaurant/"
            ]

    # 用户登录
    cookie = {
        'ubt_ssid': '1fyb3wt314fl9ur1vw4uhj11schju6wt_2018-11-08',
        '_utrace': '17844aed10e026c61611bd3aef2c3380_2018-11-08',
        'cna': 'Sb5ZFMnljzACAcpxvf7jTm61',
        'eleme__ele_me' : 'dc175d478a46cdb86a8adc8c6d8eb6f2%3A775ba4c2cf4cb5916d79ce2da6d39deb8555df2e',
        'track_id': '1541746072|5d572f1ccda6578502e5fb4a747b2beb14207cfaeab6bff882|cb40928f9d897d31ec00821132a43d95',
        'USERID': '4299687778',
        'SID': 'HzFlLzTUI23Jm7gawc43fEH0AjSoh00brVeg',
        'isg': 'BGVlVBIqUoH8aLZd-oSAmqT8dCgztUv7PieqoWdL0ByrfoDwPfACBWA_DOII_jHs'
        }

    # 访问头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive'
        }

    # 提交表单, 访问商家信息
    CountFormData = {
        'latitude': '38.55',
        'longitude': '116.7'
    }

    ShopFormData = {
        'extras[]': 'activities',
        'geohash': 'wwgmve3gb751',
        'latitude': '38.998005',
        'limit': '24',
        'longitude': '117.31443',
        'offset': '0',
        'terminal': 'web'
    }

    RateFormData = {
        'limit': '10',
        'offset': '0',
        'record_type': '1'
    }
    
    # ShopCount 用来统计不同类型的商店数量
    ShopCount = {
        'MeiShi': 0,
        'KuaiCanBianDang': 0,
        'TeSeCaiXi': 0,
        'YiGuoLiaoLi': 0,
        'XiaoChiYeXiao': 0,
        'TianPinYinPin': 0,
        'GuoShuShengXian': 0,
        'ShangDianChaoShi': 0,
        'XianHuaLvZhi': 0,
        'YiYaoJianKang': 0,
        'ZaoCan': 0,
        'WuCan': 0,
        'XiaWuCha': 0,
        'WanCan': 0,
        'YeXiao': 0
    }

    # 开始访问页面
    # 天津市位于东经116°42"~118°04", 北纬38°33"~40°15"
    def start_requests(self):
        latitude_start = 38.550000
        latitude_end = 40.250000
        longitude_start = 116.700000
        longitude_end = 118.070000

        la = latitude_start
        while (la < 40.25):
            lo = longitude_start
            while (lo < 118.07):
                self.CountFormData['latitude'] = str(la)
                self.CountFormData['longitude'] = str(lo)
                yield scrapy.FormRequest(url = self.start_urls[0], headers = self.headers, cookies = self.cookie, formdata = self.CountFormData, method = 'GET', callback = self.parse_shop_num)
                lo = lo + 0.02740              
            la = la + 0.08500

    # 统计各个类型商店数量, 并访问每一个网格点的网址
    def parse_shop_num(self, response):
        shop_num = json.loads(response.body)

        MeiShiTmp = 0
        KuaiCanBianDangTmp = 0
        TeSeCaiXiTmp = 0
        YiGuoLiaoLiTmp = 0
        XiaoChiYeXiaoTmp = 0
        TianPinYinPinTmp = 0
        GuoShuShengXianTmp = 0
        ShangDianChaoShiTmp = 0
        XianHuaLvZhiTmp = 0
        YiYaoJianKangTmp = 0
        ZaoCanTmp = 0
        WuCanTmp = 0
        XiaWuChaTmp = 0
        WanCanTmp = 0
        YeXiaoTmp = 0

        for shop in shop_num:
            # print self.ShopCount            
            # 美食
            if shop['name'] == u'\u7f8e\u98df':
                self.ShopCount['MeiShi'] = self.ShopCount['MeiShi'] + shop['count']
                MeiShiTmp = MeiShiTmp + shop['count']

            # 快餐便当
            elif shop['name'] == u'\u5feb\u9910\u4fbf\u5f53':
                self.ShopCount['KuaiCanBianDang'] = self.ShopCount['KuaiCanBianDang'] + shop['count']
                KuaiCanBianDangTmp = KuaiCanBianDangTmp + shop['count']

            # 特色菜系
            elif shop['name'] == u'\u7279\u8272\u83dc\u7cfb':
                self.ShopCount['TeSeCaiXi'] = self.ShopCount['TeSeCaiXi'] + shop['count']
                TeSeCaiXiTmp = TeSeCaiXiTmp + shop['count']

            # 异国料理
            elif shop['name'] == u'\u5f02\u56fd\u6599\u7406':
                self.ShopCount['YiGuoLiaoLi'] = self.ShopCount['YiGuoLiaoLi'] + shop['count']
                YiGuoLiaoLiTmp = YiGuoLiaoLiTmp + shop['count']

            # 小吃夜宵
            elif shop['name'] == u'\u5c0f\u5403\u591c\u5bb5':
                self.ShopCount['XiaoChiYeXiao'] = self.ShopCount['XiaoChiYeXiao'] + shop['count']
                XiaoChiYeXiaoTmp = XiaoChiYeXiaoTmp + shop['count']

            # 甜品饮品
            elif shop['name'] == u'\u751c\u54c1\u996e\u54c1':
                self.ShopCount['TianPinYinPin'] = self.ShopCount['TianPinYinPin'] + shop['count']
                TianPinYinPinTmp = TianPinYinPinTmp + shop['count']

            # 果蔬生鲜
            elif shop['name'] == u'\u679c\u852c\u751f\u9c9c':
                self.ShopCount['GuoShuShengXian'] = self.ShopCount['GuoShuShengXian'] + shop['count']
                GuoShuShengXianTmp = GuoShuShengXianTmp + shop['count']

            # 商店超市
            elif shop['name'] == u'\u5546\u5e97\u8d85\u5e02':
                self.ShopCount['ShangDianChaoShi'] = self.ShopCount['ShangDianChaoShi'] + shop['count']
                ShangDianChaoShiTmp = ShangDianChaoShiTmp + shop['count']

            # 鲜花绿植
            elif shop['name'] == u'\u9c9c\u82b1\u7eff\u690d':
                self.ShopCount['XianHuaLvZhi'] = self.ShopCount['XianHuaLvZhi'] + shop['count']
                XianHuaLvZhiTmp = XianHuaLvZhiTmp + shop['count']

            # 医药健康
            elif shop['name'] == u'\u533b\u836f\u5065\u5eb7':
                self.ShopCount['YiYaoJianKang'] = self.ShopCount['YiYaoJianKang'] + shop['count']
                YiYaoJianKangTmp = YiYaoJianKangTmp + shop['count']

            # 早餐
            elif shop['name'] == u'\u65e9\u9910':
                self.ShopCount['ZaoCan'] = self.ShopCount['ZaoCan'] + shop['count']
                ZaoCanTmp = ZaoCanTmp + shop['count']

            # 午餐
            elif shop['name'] == u'\u5348\u9910':
                self.ShopCount['WuCan'] = self.ShopCount['WuCan'] + shop['count']
                WuCanTmp = WuCanTmp + shop['count']

            # 下午茶
            elif shop['name'] == u'\u4e0b\u5348\u8336':
                self.ShopCount['XiaWuCha'] = self.ShopCount['XiaWuCha'] + shop['count']
                XiaWuChaTmp = XiaWuChaTmp + shop['count']

            # 晚餐
            elif shop['name'] == u'\u665a\u9910':
                self.ShopCount['WanCan'] = self.ShopCount['WanCan'] + shop['count']
                WanCanTmp = WanCanTmp + shop['count']

            # 夜宵
            elif shop['name'] == u'\u591c\u5bb5':
                self.ShopCount['YeXiao'] = self.ShopCount['YeXiao'] + shop['count']
                YeXiaoTmp = YeXiaoTmp + shop['count']

            # 全部商家
            elif shop['name'] == u'\u5168\u90e8\u5546\u5bb6':
                continue

            else:
                print "Shop type error."

        item = TypeItem()

        item['MeiShi'] = MeiShiTmp
        item['KuaiCanBianDang'] = KuaiCanBianDangTmp
        item['TeSeCaiXi'] = TeSeCaiXiTmp
        item['YiGuoLiaoLi'] = YiGuoLiaoLiTmp
        item['XiaoChiYeXiao'] = XiaoChiYeXiaoTmp
        item['TianPinYinPin'] = TianPinYinPinTmp
        item['GuoShuShengXian'] = GuoShuShengXianTmp
        item['ShangDianChaoShi'] = ShangDianChaoShiTmp
        item['XianHuaLvZhi'] = XianHuaLvZhiTmp
        item['YiYaoJianKang'] = YiYaoJianKangTmp
        item['ZaoCan'] = ZaoCanTmp
        item['WuCan'] = WuCanTmp
        item['XiaWuCha'] = XiaWuChaTmp
        item['WanCan'] = WanCanTmp
        item['YeXiao'] = YeXiaoTmp

        yield item

        # 商家总数
        total_offset = shop_num[0]['count']

        # 提取url中的经纬度坐标信息
        url = response.url
        la = re.findall(r".*latitude=(.*)&.*", url)[0]
        lo = re.findall(r"longitude=(.*)", url)[0]

        # 生成geohash值
        geohash = geohash2.encode(float(la), float(lo))
        
        for offset in range(0, total_offset, 24):
            self.ShopFormData['geohash'] = str(geohash)
            self.ShopFormData['latitude'] = str(la)
            self.ShopFormData['longitude'] = str(lo)
            self.ShopFormData['offset'] = str(offset)
            yield scrapy.FormRequest(url = self.start_urls[1], headers = self.headers, cookies = self.cookie, formdata = self.ShopFormData, method = 'GET', callback = self.parse_shop_info)

    def parse_shop_info(self, response):
        shop_info = json.loads(response.body)

        for shop in shop_info:
            item = WaimaiItem()
            item['id'] = shop['id']
            item['name'] = shop['name']
            item['latitude'] = shop['latitude']
            item['longitude'] = shop['longitude']
            item['float_delivery_fee'] = shop['float_delivery_fee']
            item['float_minimum_order_amount'] = shop['float_minimum_order_amount']
            item['opening_hours'] = shop['opening_hours']
            item['rating'] = shop['rating']
            item['rating_count'] = shop['rating_count']
            item['recent_order_num'] = shop['recent_order_num']
            item['flavors'] = shop['flavors']
            yield item

            # 获取评价数量
            idTmp = shop['id']
            urlTmp = self.start_urls[2] + str(idTmp) + "/rating_categories"
            yield scrapy.FormRequest(url = urlTmp, headers = self.headers, cookies = self.cookie, callback = self.parse_shop_rate_num)

    def parse_shop_rate_num(self, response):
        shop_rate_num = json.loads(response.body)
        total_offset = shop_rate_num[0]['amount']
        # print "num is : " + str(shop_rate_num[0]['amount'])
        
        url = response.url
        idTmp = re.findall(r".*restaurant/(.*)/rating_categories", url)[0]
        urlTmp = self.start_urls[2] + str(idTmp) + "/ratings?"
        for offset in range(0, total_offset, 10):
            self.RateFormData['offset'] = str(offset)
            yield scrapy.FormRequest(url = urlTmp, headers = self.headers, cookies = self.cookie, formdata = self.RateFormData, method = 'GET', callback = self.parse_shop_rate)

    def parse_shop_rate(self, response):
        shop_rate = json.loads(response.body)

        for rate in shop_rate:
            item = RateItem()
            item['rate'] = rate['rating_text']
            if len(item['rate']) != 0:
                yield item