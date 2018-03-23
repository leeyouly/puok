# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_GangguItem
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

#扑克财经需求--钢股网数据抓取
class PuokSteel(scrapy.Spider):
    name = "spd_t_puok_ganggu"
    start_urls = (
        'http://news.gangguwang.com/fastnews/fastnews',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'钢谷网')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_steel'])
        #找到4个不同类型对应的key
        pagetypeDict = {'jiage':u'价格','kucun':u'库存', 'gangchang':u'钢厂', 'hongguan':u'宏观', }
        for key in pagetypeDict:
            #拼接url用的是dict的key，传值到response用的是dict的value
            url = 'http://news.gangguwang.com/fastnews/fastnews?typeText='+ key +'&city=0'
            request = scrapy.http.FormRequest(url, callback=self.parse_content)
            request.meta['pagetype'] = pagetypeDict[key]
            yield request

    #处理返回的请求
    def parse_content(self, response):
        pagetype = response.meta['pagetype']
        contentStr = response.body
        infoListHtml = response.xpath('//div[@class="main"]/div[@class="year"]')
        for infoHtml in infoListHtml:
            idList = infoHtml.xpath('./div[@class="list"]/ul/li/div/a/@id').extract()
            infoList = infoHtml.xpath('./div[@class="list"]/ul/li/div/div/p/text()').extract()
            dataList = infoHtml.xpath('./h2/a/text()').extract()
            datadatastr = dataList[0].replace(u'年','-').replace(u'月','-').replace(u'日','')
            timeList = infoHtml.xpath('./div[@class="list"]/ul/li/p/text()').extract()
            for row in range(len(idList)):
                item = Puok_GangguItem()
                datadate = datetime.datetime.strptime(datadatastr + ' '+ timeList[row] + ':00', '%Y-%m-%d %H:%M:%S')
                item['datadate'] = datadate
                item['data_type'] = pagetype
                item['news_contents'] = infoList[row]
                item['pageid'] = idList[row]
                yield item
