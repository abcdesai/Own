# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.http import Request
import datetime
import socket
from cases.items import CasesItem


class FedappealsSpider(scrapy.Spider):
    name = "fedappeals"
    allowed_domains = ["http://www.cafc.uscourts.gov"]
    start_urls = (
        'http://www.cafc.uscourts.gov/opinions-orders',
    )

#file:///C:/opinions-orders?populate=&field_origin_value=All&field_report_type_value=All&field_date_value_1[min]
    # [value]=2002-02-08%2019%3A36%3A41&field_date_value_1[max][value]=2017-02-08%2019%3A36%3A41&field_date_dropdown=
    # date_range&page=1
    def parse(self, response):
        item_selector1st = response.xpath('//td//a/@href')

        for url in item_selector1st.extract():
            yield Request(urlparse.urljoin(response.url, ''.join(url)),
                          meta= {'urlkeys':urlparse.urljoin(response.url, ''.join(url))},callback=self.parse_pg2)

        item_selector2nd = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pager-next", " " ))]//a/@href')
        for url in item_selector2nd.extract():
            yield Request(urlparse.urljoin(response.url, ''.join(url)), meta={'pg1': url})




    def parse_pg2(self, response):
        item = CasesItem()
        title = response.xpath('//*[(@id = "headline")]/text()')
        title = ''.join(title.extract())
        item['PDF'] = 'PDF'
        item['pg1'] = response.meta['pg1']
        item['page3'] = socket.gethostname()

        item['scrape_time'] = datetime.datetime.now()
        item["spider"] = self.name
        item["file_urls"] = response.meta['urlkeys']
        return item
