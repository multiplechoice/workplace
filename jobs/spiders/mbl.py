import scrapy

from jobs.items import JobsItem
from jobs.common import decode_date_string


class MblSpider(scrapy.Spider):
    name = "mbl"
    start_urls = ['http://www.mbl.is/atvinna/']

    def parse(self, response):
        for job in response.css('.item-wrapper'):
            item = JobsItem()
            item['title'] = job.css('.title::text').extract_first()
            item['company'] = job.css('div.company-wrapper span.company::text').extract_first()
            item['deadline'] = decode_date_string(job.css('span.date::text').extract_first())

            url = response.urljoin(job.css('a::attr(href)').extract_first())
            item['url'] = url

            request = scrapy.Request(url, callback=self.parse_specific_job)
            request.meta['item'] = item
            yield request

    def parse_specific_job(self, response):
        item = response.meta['item']
        item['posted'] = decode_date_string(response.css('.ad_created::text').re(r'Sett inn: (.+)')[0])
        yield item