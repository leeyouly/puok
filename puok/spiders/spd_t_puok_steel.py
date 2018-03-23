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

#扑克财经需求--抓取钢铁数据
class PuokSteel(scrapy.Spider):
    name = "spd_t_puok_steel"
    start_urls = (
        'http://www.mysteel.com/zhibo/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'我的钢铁')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_steel'])
        #找到4个不同类型对应的key
        channelDict = {'0103':u'价格速递', '0101':u'宏观产经', '0105':u'钢厂资讯', '0104':u'库存信息',}
        #抓取最近3个页面的新闻
        for page in range(1,50,1):
            for key in channelDict:
                #拼接url用的是dict的key，传值到response用的是dict的value
                url = 'http://m.mysteel.com/v4/app/article/zhibo.ms?channelId='+key\
                      +'&pageNo='+str(page)+'&time='+day_datadate+\
                      '&content=&callback=$callback&_=1514858618324'
                request = scrapy.http.FormRequest(url, callback=self.parse_content)
                request.meta['channel'] = channelDict[key]
                yield request

    #处理返回的请求
    def parse_content(self, response):
        contentStr = response.body
        #判断一下返回的内容长度是否大于20个字节，小于20个字节则认为其是不规范数据，不予处理
        if len(contentStr) > 20:
            #根据网页返回值的内容，截取中间需要的数据，转换为list，再做处理。
            contentList = eval(re.findall('callback(.+);',contentStr)[0])
            channel = response.meta['channel']
            for data in contentList['data']:
                item = Puok_SteelItem()
                datadate = datetime.datetime.strptime(data['time'] + ' ' + data['time1'] + ':00', '%Y-%m-%d %H:%M:%S')
                item['datadate'] = datadate
                item['data_type'] = channel
                item['news_contents'] = data['title']
                item['pageid'] = data['id']
                yield item