# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_cansiItem
import re
import random
import lxml
import time, datetime
import sys
from puok.table import table_to_list
reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now()
day_datadate = today.strftime('%Y-%m-%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=10)

index = 1

#扑克财经需求--中国船舶工业行业协会
class PuokCSRC(scrapy.Spider):
    name = "spd_t_puok_cansi"
    start_urls = (
        'http://www.cansi.org.cn/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'中国船舶工业行业协会')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_cansi'])

        # url = 'http://www.nea.gov.cn/20140521_1449.pdf'
        # request = scrapy.http.FormRequest(url, callback=self.parse_title)
        # yield request

        for page in range(1,2,1):
            titleurl = 'http://www.cansi.org.cn/index.php/Information/index/pid/1/PHPSESSID/' \
                       'cc41796507a7d056d381d0c3f2aeb683/p/'+ str(page) +'.html'
            request = scrapy.http.Request(titleurl, callback=self.parse_title)
            yield request

    #解析文章标题以及url
    def parse_title(self, response):
        newsUl = response.xpath('//*[@id="a1"]/ul//li')
        # response.xpath('//*[@id="a1"]/ul/li[2]/a/text()')
        for newsList in newsUl:
            if newsList.xpath('./a/@href').extract() <> []:
                datadate = newsList.xpath('./em/text()').extract()[0]
                # newsTitle = newsList.xpath('./a/text()').extract()[0].strip()
                newsContentURL =  response.urljoin(newsList.xpath('./a/@href').extract()[0])

                request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
                request.meta['datadate'] = datadate.strip()
                # request.meta['newsTitle'] = newsTitle
                request.meta['newsContentURL'] = newsContentURL
                yield request
            else:
                print u'未找到url,暂停3到5秒重新请求--->' + response.url
                # time.sleep(random.uniform(3, 5))
                request = scrapy.http.Request(response.url, callback=self.parse_title)
                yield request

    #解析文章内容
    def parse_newsContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y-%m-%d')
        # imageurl = ''
        # newsTitle = response.meta['newsTitle']
        # newsContentURL = response.meta['newsContentURL']

        data_table = response.xpath('//*[@id="main-right"]/div[@class="right03"]/table')
        data_list = table_to_list(data_table)

        for data in data_list[1:]:
            item = Puok_cansiItem()
            item['datadate'] = data[0].replace('\n','').replace('\t','').replace('\r','-')
            item['index_name'] = data[1]
            item['world'] = data[2].replace('%','')
            item['china'] = data[3].replace('%','')
            item['korea'] = data[4].replace('%','')
            item['japan'] = data[5].replace('%','')
            item['update_dt'] = datetime.datetime.now()
            item['source'] = response.url
            yield item


