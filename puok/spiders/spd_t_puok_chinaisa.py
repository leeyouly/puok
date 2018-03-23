# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_chinaisaItem
import re
import lxml
from lxml import etree
import time, datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

today = datetime.datetime.now()
day_datadate = today.strftime('%Y-%m-%d')
year_datadate = today.strftime('%Y')
last_year = int(year_datadate) - 1
last_update_date = datetime.datetime.now() - datetime.timedelta(days=10)

#扑克财经需求--中国钢铁工业协会网--市场分析和行业要闻
class PuokChinaisa(scrapy.Spider):
    name = "spd_t_puok_chinaisa"
    start_urls = (
        'http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&key=' \
              'UzBcY1oxVjdWN1ViUTYAYQJmUzBUMAYxUmFRZFIwAjQKGQpFARpSYFRFAUYAF1Aw',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'中国钢铁工业协会网--市场分析--行业要闻')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_chinaisa'])
        url = 'http://www.chinaisa.org.cn/gxportal/EiService'
        #402 市场发现 213 行业要闻
        # nodeIdList = ['213','402','395','212','495']
        nodeIdList = ['495']
        for nodeId in nodeIdList:
            if nodeId == '402':
                sumPage = 39
            elif nodeId == '213':
                sumPage = 1468
            elif nodeId == '395':
                sumPage = 53
            elif nodeId == '212':
                sumPage = 9
            elif nodeId == '495':
                sumPage = 6
            for page in range(sumPage):
                form_data = {
                    'service': 'ECTM02',
                    'method': 'turnPage',
                    'eiinfo': '{attr:{"templateUnitInsId":"0000000000010086","nodeId":"0000000000000'+nodeId+'","nodeType":'
                              '"c","":"'+str(page+1)+'","currentPage":'+str(page+1)+'},blocks:{}}',
                }
                request = scrapy.http.FormRequest(url, callback=self.parse_title,formdata=form_data)
                request.meta['nodeId'] = nodeId
                yield request

    #解析文章标题以及拿到下一步框架的url，这个url用来寻找真正的文章地址
    def parse_title(self, response):
        contentStr = response.body
        contentHtml = eval(contentStr)
        str1 = contentHtml['attr']['pageString']
        page = etree.HTML(str1.decode('utf-8'))
        title_list = page.xpath("//div/table//tr")
        index = 0
        for title in title_list :
            if title.xpath('./td/div/a/@href') <> []:
                contentFrame_url = response.urljoin(title.xpath('./td/div/a/@href')[0])
                title_name = title.xpath('./td/div/a/text()')[0].strip()
                title_date = title.xpath('./td/div/a/span/text()')[0].strip()
                request = scrapy.http.Request(contentFrame_url, callback=self.parse_newsFrameContent)
                request.meta['title_name'] = title_name
                request.meta['title_date'] = title_date
                request.meta['nodeId'] = response.meta['nodeId']
                yield request
            else:
                print u'第 ' + str(index) + u' 次循环未解析到数据，初始url---> ' + response.url
            index = index + 1

    #解析文章内容或者拿到文章内容的真实地址
    def parse_newsFrameContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['title_date'], '%Y-%m-%d')
        realUrlPart = response.xpath('//*[@id="mframe"]/@src')
        #如果不等于空，表示此页面不含有文章，文章需要去另外一个页面取到
        # 中国钢铁业协会网站比较特殊，要先解析这个网页框架，从框架中拿出真正的html文章的地址，才能继续解析
        if realUrlPart <> []:
            #realURL才是真正文章位置的url
            realURL = response.urljoin(realUrlPart.extract()[0])
            request = scrapy.http.Request(realURL, callback=self.parse_newsContent)
            request.meta['title_name'] = response.meta['title_name']
            request.meta['datadate'] = datadate
            request.meta['frameURL'] = response.url
            request.meta['nodeId'] = response.meta['nodeId']
            yield request
        elif response.xpath('//table[@class="subpage_inftitle_1_table"]') <> []:
            item = Puok_chinaisaItem()
            item['datadate'] = datadate
            nodeId = response.meta['nodeId']
            if nodeId == '402':
                item['news_type'] = u'市场发现'
            elif nodeId == '213':
                item['news_type'] = u'行业要闻'
            elif nodeId == '395':
                item['news_type'] = u'铁矿石价格指数'
            elif nodeId == '212':
                item['news_type'] = u'中钢协-销量，库存'
            elif nodeId == '495':
                item['news_type'] = u'中钢协-厂库，社库'
            item['news_title'] = response.meta['title_name']
            item['news_contentframeurl'] = ''
            #满足此条件的新闻frameurl就是真实的url
            item['news_contentrealurl'] = response.url
            item['image_url'] = ''
            # item['update_dt'] = today.strptime('%Y-%m-%d %H:%M:%S')
            item['update_dt'] = datetime.datetime.now()
            item['html_news'] = response.xpath('//table[@class="subpage_inftitle_1_table"]').extract()[0]
            yield item
        else:
            print u'可能未采集到的url--real----->' + response.url

    #解析文章内容
    #.decode('unicode_escape')
    def parse_newsContent(self,response):
        contentList = response.xpath('//div[@class="Section1"]').extract()
        if contentList <> []:
            #\xd6\xd0\xb9\xfa\xcc\xfa\xbf\xf3\xca\xaf\xbc\xdb\xb8\xf1\xd6\xb8\xca\xfd\xa3\xa8
            html_news = response.xpath('//div[@class="Section1"]')[0].extract()
            # html_parser = lxml.html.HTMLParser(encoding='gbk', remove_comments=True)
            # content_html_etree = lxml.html.fromstring(html_news, parser=html_parser)
            # lxml.etree.strip_elements(content_html_etree, 'iframe', 'script', 'style')
            # html_news = lxml.html.tostring(content_html_etree, encoding='utf-8').decode('utf-8')

            nodeId = response.meta['nodeId']
            item = Puok_chinaisaItem()
            item['datadate'] = response.meta['datadate']
            if nodeId == '402':
                item['news_type'] = u'市场发现'
            elif nodeId == '213':
                item['news_type'] = u'行业要闻'
            elif nodeId == '395':
                item['news_type'] = u'铁矿石价格指数'
            elif nodeId == '212':
                item['news_type'] = u'中钢协-销量，库存'
            elif nodeId == '495':
                item['news_type'] = u'中钢协-厂库，社库'
            item['news_title'] = response.meta['title_name']
            item['news_contentframeurl'] = response.meta['frameURL']
            item['news_contentrealurl'] = response.url
            item['image_url'] = ''
            # item['update_dt'] = today.strptime('%Y-%m-%d %H:%M:%S')
            item['update_dt'] = datetime.datetime.now()
            if nodeId == '395':
                item['html_news'] = unicode(response.body, 'gb2312')
            else:
                item['html_news'] = contentList[0]

            yield item
        else:
            print u'未解析到文章内容,url为---->' + response.url

