# -*- coding: UTF-8 -*-
import scrapy
from puok.items import Puok_chinaisaPartpriceItem
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

#扑克财经需求--中国钢铁工业协会网--地区价格
class PuokChinaisa(scrapy.Spider):
    name = "spd_t_puok_chinaisa_partprice"
    start_urls = (
        'http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&'
        'key=VjVbZAxnAGEFZA45AmVQMVA0UDMDZ1BnUmEJPFg6BDMEF1oVARoCMFFAUBcFElY2###',
    )
    ignore_page_incremental = True

    def parse(self,response):
        self.crawler.stats.set_value('spiderlog/source_name', u'中国钢铁工业协会网--地区价格')
        self.crawler.stats.set_value('spiderlog/target_tables', ['t_puok_chinaisa'])
        url = 'http://www.chinaisa.org.cn/gxportal/EiService'
        #403 地区价格
        nodeIdList = ['403']
        for nodeId in nodeIdList:
            if nodeId == '403':
                sumPage = 5
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

    #解析文章内容或者拿到文章内容的真实地址
    def parse_newsFrameContent(self, response):
        datadate = datetime.datetime.strptime(response.meta['title_date'], '%Y-%m-%d')
        realUrlPart = response.xpath('//*[@id="mframe"]/@src')
        #如果不等于空，表示此页面不含有文章，文章需要去另外一个页面取到
        # 中国钢铁业协会网站比较特殊，要先解析这个网页框架，从框架中拿出真正的html文章的地址，才能继续解析
        #/html/body/table
        if realUrlPart <> []:
            #realURL才是真正文章位置的url
            realURL = response.urljoin(realUrlPart.extract()[0])
            request = scrapy.http.Request(realURL, callback=self.parse_newsContent)
            request.meta['title_name'] = response.meta['title_name']
            request.meta['datadate'] = datadate
            request.meta['frameURL'] = response.url
            request.meta['nodeId'] = response.meta['nodeId']
            yield request
        #也有部分页面数据就在此页面
        else:
            data_table = response.xpath('//*[@id="wrapper"]/table[2]/tr[3]/td/table/tr[3]/td/table')
            data_list = table_to_list(data_table)
            # nodeId = response.meta['nodeId']
            if data_list <> []:
                for data in data_list[1:]:
                    if data[0] <> '':
                        for rows in range(2, len(data_list[1]), 1):
                            item = Puok_chinaisaPartpriceItem()
                            item['datadate'] = datadate
                            item['page_date'] = response.meta['title_name']
                            # item['page_title'] = response.meta['title_name']
                            item['unit'] = u'元/吨'
                            item['part'] = data_list[0][rows]
                            item['mainsort'] = data[0]
                            item['mainsize'] = data[1]
                            item['price'] = data[rows]
                            item['update_dt'] = datetime.datetime.now()
                            item['source'] = response.url
                            yield item
            else:
                print u'未找到首次解析页面的table--->' + response.meta['title_name'] + ' ' + response.url

    #解析文章内容
    def parse_newsContent(self,response):
        #现在拿到的可能还不是真正的table地址，需要再次解析table的实际地址
        realdataherf = response.xpath('//*[@id="shLink"]/@href').extract()
        if realdataherf <> []:
            realdataURL = response.urljoin(realdataherf[0])
            request = scrapy.http.Request(realdataURL, callback=self.parse_table)
            request.meta['datadate'] = response.meta['datadate']
            request.meta['title_name'] = response.meta['title_name']
            yield request
        else:
            data_table = response.xpath('/html/body/div/table')
            data_list = table_to_list(data_table)
            # nodeId = response.meta['nodeId']
            if data_list <> []:
                for data in data_list[1:]:
                    if data[0] <> '':
                        for rows in range(2, len(data_list[1]), 1):
                            item = Puok_chinaisaPartpriceItem()
                            item['datadate'] = response.meta['datadate']
                            item['page_date'] = response.meta['title_name']
                            item['unit'] = u'元/吨'
                            item['part'] = data_list[0][rows]
                            item['mainsort'] = data[0]
                            item['mainsize'] = data[1]
                            item['price'] = data[rows]
                            item['update_dt'] = datetime.datetime.now()
                            item['source'] = response.url
                            yield item
            else:
                print u'parse_newsContent 方法中未解析到数据--->' + response.meta['title_name'] + ' ' + response.url


    def parse_table(selfs,response):
        url = response.url
        data_table = response.xpath('/html/body/table')
        data_list = table_to_list(data_table)
        # nodeId = response.meta['nodeId']
        if data_list <> []:
            for data in data_list[4:10]:
                if data[0] <> '':
                    for rows in range(2,len(data_list[3]),1):
                        item = Puok_chinaisaPartpriceItem()
                        item['datadate'] = response.meta['datadate']
                        item['page_date'] = data_list[0][0]
                        # item['unit'] = data_list[1][13]
                        item['unit'] = u'元/吨'
                        item['part'] = data_list[2][rows]
                        item['mainsort'] = data[0]
                        item['mainsize'] = data[1]
                        item['price'] = data[rows]
                        item['update_dt'] = datetime.datetime.now()
                        item['source'] = url
                        yield item

        else:
            print u'进入了table的数据页，但xpath未找到数据位置' + response.meta['title_name'] + ' ' + response.url

