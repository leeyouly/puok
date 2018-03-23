# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_chinaisaSortpriceItem
import re
import lxml
from lxml import etree
import time, datetime
from puok.table import table_to_list
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
    name = "spd_t_puok_chinaisa_sortprice"
    start_urls = (
        'http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&'
        'key=VzQJNlw3UDECY1RjAGcAYVE1UDNUMAM0BTYJPABmBzJXRAlGCxAAMgITVRJSRVIy',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'中国钢铁工业协会网--主要产品价格指数')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_chinaisa'])
        url = 'http://www.chinaisa.org.cn/gxportal/EiService'
        #441 主要产品价格指数
        # nodeIdList = ['213','402']
        nodeIdList = ['441']
        for nodeId in nodeIdList:
            if nodeId == '441':
                sumPage = 35
            for page in range(0,3,1):
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
                # print u'第 ' + str(index) + u' 次循环未解析到数据，初始url---> ' + response.url
                pass
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
        #table数据就在此页
        else:
            #找page_sort
            # page_sort1 = response.xpath('//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/p[3]/span//text()').extract()
            # page_sort2 = response.xpath('//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/p[5]/span//text()').extract()
            # if page_sort1 == [] and page_sort2 == []:
            #     page_sort1 = response.xpath(
            #         '//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/div[1]//text()').extract()
            #     page_sort2 = response.xpath(
            #         '//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/div[2]//text()').extract()
            #     if page_sort1 <> [] and page_sort2 <> []:
            #         page_sort1 = page_sort1[0]
            #         page_sort2 = page_sort2[0]
            #     else:
            #         print u'找不到标题了。。。' + response.url
            # else:
            #     page_sort1 = page_sort1[0]
            #     page_sort2 = page_sort2[0]

            data_table1 = response.xpath('//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/table[1]')
            data_list1 = table_to_list(data_table1)

            # nodeId = response.meta['nodeId']
            if data_list1 <> []:
                for data in data_list1[2:]:
                    for rows in range(2, 8, 1):
                        item = Puok_chinaisaSortpriceItem()
                        item['datadate'] = datadate
                        item['page_date'] = response.meta['title_name']
                        item['page_sort'] = u'国内市场八个品种价格及指数（含税价）'
                        if rows < 6:
                            item['index_name'] = data_list1[0][rows] + ' ' + data_list1[1][rows]
                        else:
                            item['index_name'] = data_list1[0][rows]
                        item['mainsort'] = data[0]
                        item['mainsize'] = data[1]
                        item['price'] = data[rows]
                        item['update_dt'] = datetime.datetime.now()
                        item['source'] = response.url
                        yield item
            else:
                print u'parse_newsFrameContent function, data_list1-->' + response.url

            data_table2 = response.xpath('//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/table[2]')
            data_list2 = table_to_list(data_table2)
            if data_list2 <> []:
                for data in data_list2[2:]:
                    for rows in range(1, 5, 1):
                        item = Puok_chinaisaSortpriceItem()
                        item['datadate'] = datadate
                        item['page_date'] = response.meta['title_name']
                        item['page_sort'] = u'国内市场钢材综合价格指数及长材、板材价格指数（含税）'
                        if rows < 3:
                            item['index_name'] = data_list2[0][rows] + ' ' + data_list2[1][rows]
                        else:
                            item['index_name'] = data_list2[0][rows]
                        item['mainsort'] = data[0]
                        item['mainsize'] = u'无规格'
                        item['price'] = data[rows]
                        item['update_dt'] = datetime.datetime.now()
                        item['source'] = response.url
                        yield item
            else:
                print u'parse_newsFrameContent function, data_list2-->' + response.url


    #解析文章内容
    def parse_newsContent(self,response):
        #现在拿到的可能还不是真正的table地址，需要再次解析table的实际地址
        realherf = response.xpath('//*[@id="shLink"]/@href').extract()
        if realherf <> []:
            realURL = response.urljoin(realherf[0])
            # print 'table realURL--->' + realURL
            request = scrapy.http.Request(realURL, callback=self.parse_table)
            request.meta['datadate'] = response.meta['datadate']
            yield request
        else:
            # print 'parse_newsContent function error + ' + response.url
            page_sort1 = response.xpath('/html/body/div/p[1]/span/text()').extract()
            page_sort2 = response.xpath('/html/body/div/p[2]/span/text()').extract()
            if page_sort1 <> [] and page_sort2 <> [] :
                page_sort1 = page_sort1[0]
                page_sort2 = page_sort2[0]

            data_table1 = response.xpath('/html/body/div/div[1]/table')
            if data_table1.extract() == []:
                data_table1 = response.xpath('/html/body/div/table[1]')

            data_list1 = table_to_list(data_table1)

            # nodeId = response.meta['nodeId']
            if data_list1 <> []:
                for data in data_list1[2:]:
                    for rows in range(2, 8, 1):
                        item = Puok_chinaisaSortpriceItem()
                        item['datadate'] = response.meta['datadate']
                        item['page_date'] = response.meta['title_name']
                        item['page_sort'] = page_sort1
                        if rows < 6:
                            item['index_name'] = data_list1[0][rows] + ' ' + data_list1[1][rows]
                        else:
                            item['index_name'] = data_list1[0][rows]
                        item['mainsort'] = data[0]
                        item['mainsize'] = data[1]
                        item['price'] = data[rows]
                        item['update_dt'] = datetime.datetime.now()
                        item['source'] = response.url
                        yield item
            else:
                print u'parse_newsContent function, data_list1-->' + response.url

            data_table2 = response.xpath('/html/body/div/div[2]/table')
            if data_table2.extract() == []:
                data_table2 = response.xpath('/html/body/div/table[2]')

            data_list2 = table_to_list(data_table2)

            if data_list2 <> []:
                for data in data_list2[2:]:
                    for rows in range(1, 5, 1):
                        item = Puok_chinaisaSortpriceItem()
                        item['datadate'] = response.meta['datadate']
                        item['page_date'] = response.meta['title_name']
                        item['page_sort'] = page_sort2
                        if rows < 3:
                            item['index_name'] = data_list2[0][rows] + ' ' + data_list2[1][rows]
                        else:
                            item['index_name'] = data_list2[0][rows]
                        item['mainsort'] = data[0]
                        item['mainsize'] = u'无规格'
                        item['price'] = data[rows]
                        item['update_dt'] = datetime.datetime.now()
                        item['source'] = response.url
                        yield item
            else:
                print u'parse_newsContent function, data_list2-->' + response.url

    def parse_table(selfs,response):
        url = response.url
        data_table = response.xpath('/html/body/table')
        data_list = table_to_list(data_table)
        # nodeId = response.meta['nodeId']
        if data_list <> []:
            for data in data_list[5:13]:
                for rows in range(2,8,1):
                    item = Puok_chinaisaSortpriceItem()
                    item['datadate'] = response.meta['datadate']
                    item['page_date'] = data_list[0][0]
                    item['page_sort'] = data_list[1][0]
                    if rows < 6:
                        item['index_name'] = data_list[3][rows] + ' ' + data_list[4][rows]
                    else:
                        item['index_name'] = data_list[3][rows]
                    item['mainsort'] = data[0]
                    item['mainsize'] = data[1]
                    item['price'] = data[rows]
                    item['update_dt'] = datetime.datetime.now()
                    item['source'] = url
                    yield item

            for data in data_list[16:19]:
                for rows in [2,4,6,7]:
                    item = Puok_chinaisaSortpriceItem()
                    item['datadate'] = response.meta['datadate']
                    item['page_date'] = data_list[0][0]
                    item['page_sort'] = data_list[13][0]
                    if rows < 6:
                        item['index_name'] = data_list[14][rows] + ' ' + data_list[15][rows]
                    else:
                        item['index_name'] = data_list[14][rows]
                    item['mainsort'] = data[0]
                    item['mainsize'] = u'无规格'
                    item['price'] = data[rows]
                    item['update_dt'] = datetime.datetime.now()
                    item['source'] = url
                    yield item
        else:
            print 'parse_table function, not find table---->' + response.url

