# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_tradeNoticeItem
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

#扑克财经需求--抓取交易所公告
class PuokChinaisa(scrapy.Spider):
    name = "spd_t_puok_tradeNotice"
    start_urls = (
        'http://www.shfe.com.cn/news/notice/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'交易所公告抓取')
        self.crawler.stats.set_value('spiderlog/target_tables', ['T_PUOK_TRADENOTICE'])
        #trade_dict分别对应
        trade_dict = {
            'url_zss':'http://www.czce.com.cn/portal/jysdt/ggytz/A090601index_',
            'url_dss':'http://www.dce.com.cn/dalianshangpin/yw/fw/jystz/ywtz/13305-',
            'url_sqs':'http://www.shfe.com.cn/news/notice/index_',
        }

        for key in trade_dict:
            if key == 'url_zss':
                for page in range(1,3,1):
                    url = trade_dict[key] + str(page) + '.htm'
                    request = scrapy.http.Request(url, callback=self.parse_zss,)
                    request.meta['title_url'] = url
                    yield request
            elif key == 'url_dss':
                for page in range(1,3,1):
                    url = trade_dict[key] + str(page) + '.html'
                    request = scrapy.http.Request(url, callback=self.parse_dss_title,)
                    request.meta['title_url'] = url
                    yield request
            elif key == 'url_sqs':
                for page in range(1,3,1):
                    if page == 1:
                        url = 'http://www.shfe.com.cn/news/notice/index.html'
                    else:
                        url = trade_dict[key] + str(page) + '.html'
                    request = scrapy.http.Request(url, callback=self.parse_sqs_title,)
                    request.meta['title_url'] = url
                    yield request

    #解析郑商所 文章标题,拿到url。 郑商所的公告全部是pdf，在数据库中只存pdf地址，不下载和解析pdf
    def parse_zss(self, response):
        title_list = response.xpath('/html/body/table[4]/tbody/tr[1]/td[4]/table[2]/tbody/tr[1]/td/table/td')
        if title_list <> []:
            for title in title_list:
                news_url = response.urljoin(title.xpath('./table/tbody/tr/td[1]/a/@href').extract()[0])
                news_title = title.xpath('./table/tbody/tr/td[1]/a/text()').extract()[0]
                news_date = title.xpath('./table/tbody/tr/td[2]/text()').extract()[0]
                item = Puok_tradeNoticeItem()
                item['datadate'] = datetime.datetime.strptime(news_date, '%Y-%m-%d')
                item['bourse'] = u'郑州商品期货交易所'
                item['news_type'] = u'公告'
                item['news_title'] = news_title
                item['news_url'] = news_url
                item['update_dt'] = datetime.datetime.now()
                #标题列表的url
                item['source'] = response.meta['title_url']
                item['html_news'] = None
                yield item
        else:
            print u'郑商所未采集到的url--->' + response.url

    #解析郑商所内容，郑商所公告为pdf，暂时不用解析，留个方法做接口放在这里
    def parse_dss_content(selfs, response):
        pass

    # 解析大连商品交易所 文章标题,拿到url。
    def parse_dss_title(self, response):
        title_list = response.xpath('//*[@id="13305"]/div[2]/ul/li')
        if title_list <> []:
            for title in title_list:
                news_url = response.urljoin(title.xpath('./a/@href').extract()[0])
                news_title = title.xpath('./a/text()').extract()[0]
                news_date = title.xpath('./span/text()').extract()[0]
                request = scrapy.http.Request(news_url, callback=self.parse_dss_content, )
                request.meta['title_url'] = news_url
                request.meta['news_title'] = news_title
                request.meta['news_date'] = news_date
                yield request
        else:
            print u'大连商品交易所未采集到的url--->' + response.url


    #解析大商所内容
    def parse_dss_content(selfs, response):
        html_news = response.xpath('//*[@id="zoom"]').extract()
        if html_news <> []:
            item = Puok_tradeNoticeItem()
            item['datadate'] = datetime.datetime.strptime(response.meta['news_date'], '%Y-%m-%d')
            item['bourse'] = u'大连商品交易所'
            item['news_type'] = u'公告'
            item['news_title'] = response.meta['news_title']
            item['news_url'] = response.url
            item['update_dt'] = datetime.datetime.now()
            # 标题列表的url
            item['source'] = response.meta['title_url']
            item['html_news'] = html_news[0]
            yield item
        else:
            print u'--大商所未解析到的新闻内容,网址为--->' + response.url


    # 解析上期所 文章标题,拿到url。
    def parse_sqs_title(self, response):
        # '//*[@id="main"]/div[@class="conncent"]/div[@class="fl"]/div[@class="internews"]/div[class="p4 lawbox"]/ul/li'
        title_list = response.xpath('//*[@id="main"]/div[@class="conncent"]/div[@class="fl"]/'
                                    'div[@class="internews"]/div[@class="p4 lawbox"]/ul/li')
        if title_list <> []:
            for title in title_list:
                news_url = response.urljoin(title.xpath('./a/@href').extract()[0])
                news_title = title.xpath('./a/text()').extract()[0]
                news_date = title.xpath('./span/text()').extract()[0].replace('[','').replace(']','')
                request = scrapy.http.Request(news_url, callback=self.parse_sqs_content, )
                request.meta['title_url'] = news_url
                request.meta['news_title'] = news_title
                request.meta['news_date'] = news_date
                yield request
        else:
            print u'上海期货交易所未采集到的url--->' + response.url

    #解析上期所公告内容
    def parse_sqs_content(selfs, response):
        # '//*[@id="main"]/div[3]/div[1]/div[1]'
        html_news = response.xpath('//*[@id="main"]/div[@class="conncent"]/div[1]/div[@class="article-detail-text"]').extract()
        if html_news <> []:
            item = Puok_tradeNoticeItem()
            item['datadate'] = datetime.datetime.strptime(response.meta['news_date'], '%Y-%m-%d')
            item['bourse'] = u'上海期货交易所'
            item['news_type'] = u'公告'
            item['news_title'] = response.meta['news_title']
            item['news_url'] = response.url
            item['update_dt'] = datetime.datetime.now()
            # 标题列表的url
            item['source'] = response.meta['title_url']
            item['html_news'] = html_news[0]
            yield item
        else:
            print u'--上海期货交易所未解析到的新闻内容,网址为--->' + response.url