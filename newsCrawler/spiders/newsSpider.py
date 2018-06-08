from scrapy.spiders import CrawlSpider
from urllib import parse
import re
from scrapy.selector import Selector
import datetime
import pymongo
from newsCrawler.settings import MONGODB_HOST
from newsCrawler.settings import MONGODB_PORT
from lxml import etree

nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 现在时刻

class newsSpider(CrawlSpider):
    name = "newsSpider"

    start_urls = ['http://www.chinanews.com']

    def parse(self, response):
        res_url = response.url
        print('现在进行到: '+res_url)

        # 此处是将爬取下来的网页以文件保存，留作备份，可以注释掉
        with open('../crawler_files/news_webs/' + nowTime + '.html', 'w') as f:
            f.write(response.text)

        selector = Selector(response=response)

        match_a_list = selector.xpath('//*/a')
        news_list = {}
        for each_match_a in match_a_list:
            a_text = str(each_match_a.xpath('./text()').extract())
            a_href = str(each_match_a.xpath('./@href').extract())
            news_list[a_text] = a_href
        print(news_list)

        #  向mongodb中插入data
        data = {
            'news_list' : news_list
        }

        # 向mongodb中插入数据，修改settings.py
        connection = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
        tdb = connection.test   # test为数据库名
        post_info = tdb.test_table  # test_table 为表名
        post_info.insert(data)