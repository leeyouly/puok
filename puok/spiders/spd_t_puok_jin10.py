# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_SteelItem
import puok.settings as settings
import cx_Oracle
import re
import time, datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now()
day_datadate = today.strftime('%Y-%m-%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=10)

#扑克财经需求--金十数据网抓取
class PuokJin10(scrapy.Spider):
    name = "spd_t_puok_jin10"
    start_urls = (
        'https://www.jin10.com/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'金十数据')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_jin10'])

        title = response.xpath('//*[@id="J_flashList"]/div/div[2]/h4').extract()

        listStr = re.findall('var flashData = (.+?);',response.body)[0]
        newsList = eval(listStr)
        for news in newsList:
            item = Puok_SteelItem()
            datadate = datetime.datetime.strptime(news.split('#')[2], '%Y-%m-%d %H:%M:%S')
            item['datadate'] = datadate
            if news.split('#')[1] == 0:
                item['data_type'] = u'重要资讯'
            elif news.split('#')[1] == 1:
                item['data_type'] = u'普通资讯'
            item['news_contents'] = news.split('#')[3]
            item['pageid'] = news.split('#')[11]
            item['update_dt'] = datetime.datetime.now()
            yield item
