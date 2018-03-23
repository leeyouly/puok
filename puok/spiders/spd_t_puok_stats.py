# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_statsItem
import re
import random
import lxml
import time, datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now()
day_datadate = today.strftime('%Y-%m-%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=10)

index = 1

#扑克财经需求--西本新干线
class PuokCSRC(scrapy.Spider):
    name = "spd_t_puok_stats"
    start_urls = (
        'http://www.stats.gov.cn/',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'国家统计局')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_stats'])

        for page in range(0,1,1):
            if page == 0:
                titleurl = 'http://www.stats.gov.cn/tjsj/xwfbh/fbhwd/index.html'
            else :
                titleurl = 'http://www.stats.gov.cn/tjsj/xwfbh/fbhwd/index_'+str(page)+'.html'

            request = scrapy.http.FormRequest(titleurl, callback=self.parse_title)
            yield request

    #解析文章标题以及url
    def parse_title(self, response):
        newsUl = response.xpath('/html/body/div/div/div[3]/div[2]/ul/li')

        # for newsList in newsUl:
        for newsDetail in newsUl:
            if newsDetail.xpath('./span/font[1]/a/text()').extract() <>[]:
                datadateStr = newsDetail.xpath('./span/font[1]/a/@href').extract()[0]
                datadate = re.findall('zxfb/(.+?)/',datadateStr)[0]
                newsTitle = newsDetail.xpath('./span/font[1]/a/text()').extract()[0]
                newsContentURL =  response.urljoin(newsDetail.xpath('./span/font[1]/a/@href').extract()[0])
                # print 'newsHref----> ' + newsHref
                # print 'response.urljoin----> ' + response.urljoin(newsHref)
                # print newsTitle
                # newsContentURL = 'http://www.ndrc.gov.cn/xwzx/xwfb/'+newsHref.replace('./','')
                request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
                request.meta['datadate'] = datadate
                request.meta['newsTitle'] = newsTitle
                request.meta['newsContentURL'] = newsContentURL
                # request.meta['news_type'] = response.meta['news_type']
                yield request

    #解析文章内容
    def parse_newsContent(self, response):
        # datadate = datetime.datetime.strptime(response.meta['datadate'], '%Y%m')
        datadate = response.meta['datadate']
        imageurl = ''
        newsTitle = response.meta['newsTitle']
        newsContentURL = response.meta['newsContentURL']
                                  # './/div/div[1]/div[3]/div[1]/div/div'
        news_html = response.xpath('.//div[@class="TRS_PreAppend"]').extract()
        if news_html == []:
            news_html = response.xpath('.//div[@class="TRS_Editor"]').extract()
            if news_html == []:
                news_html = response.xpath('.//div[@class="xilan_con"]').extract()
                if news_html <> []:
                    news_html = news_html[0]
                    # html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
                    # content_html_etree = lxml.html.fromstring(news_html, parser=html_parser)
                    # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
                    # news_html = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')
                    # print '1111111111'
                    item = Puok_statsItem()
                    item['datadate'] = datadate
                    item['news_title'] = newsTitle
                    item['news_content'] = u''
                    item['news_html'] = news_html
                    item['news_contenturl'] = newsContentURL
                    item['news_imageurl'] = imageurl
                    item['update_dt'] = datetime.datetime.now()
                    yield item

                else:
                    print u'可能是请求过快，未解析到内容，暂停3到5秒重新请求-->' + response.url
                    time.sleep(random.uniform(1, 2))
                    request = scrapy.http.Request(newsContentURL, callback=self.parse_newsContent)
                    request.meta['datadate'] = datadate
                    request.meta['newsTitle'] = newsTitle
                    request.meta['newsContentURL'] = newsContentURL
                    yield request

            else:
                news_html = news_html[0]
                # html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
                # content_html_etree = lxml.html.fromstring(news_html, parser=html_parser)
                # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
                # news_html = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')
                # print '33333333'
                item = Puok_statsItem()
                item['datadate'] = datadate
                item['news_title'] = newsTitle
                item['news_content'] = u''
                item['news_html'] = news_html
                item['news_contenturl'] = newsContentURL
                item['news_imageurl'] = imageurl
                item['update_dt'] = datetime.datetime.now()
                yield item
        else:
            news_html = news_html[0]
            # html_parser = lxml.html.HTMLParser(encoding='gb2312', remove_comments=True)
            # content_html_etree = lxml.html.fromstring(news_html, parser=html_parser)
            # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
            # news_html = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')
            # print '222222222'
            item = Puok_statsItem()
            item['datadate'] = datadate
            item['news_title'] = newsTitle
            item['news_content'] = u''
            item['news_html'] = news_html
            item['news_contenturl'] = newsContentURL
            item['news_imageurl'] = imageurl
            item['update_dt'] = datetime.datetime.now()
            yield item

