import scrapy as scrapy

from gushici.items import GushiciItem


class Gushici(scrapy.Spider):
    name = "gushici"
    domian = 'https://www.gushiwen.org'
    allowed_domians = ['https://www.gushiwen.org/']
    start_urls = ['https://www.gushiwen.org/shiwen/']

    def parse(self, response):
        # //div[@class="cont"]/p[1]/a/b
        # // div[ @ class ="left"] // div[@ class ="cont"]
        conts = response.xpath('// div[ @ class ="left"] // div[@ class ="cont"]')
        print(response.url)
        for cont in conts:
            item = GushiciItem()
            item['title'] = cont.xpath('p[1]/a/b/text()').extract_first()
            item['dynasty'] = cont.xpath('p[2]/a[1]/text()').extract_first()
            item['author'] = cont.xpath('p[2]/a[2]/text()').extract_first()
            item['content'] = cont.xpath('string(div[@class="contson"])').extract_first().replace('\n', '').replace('\u3000', '')
            # print('---------------------')
            # print('==> ', cont.xpath('div[@class="contson"]').extract_first())
            # print('++> ', cont.xpath('string(div[@class="contson"])').extract_first())
            # print('~~> ', cont.xpath('string(div[@class="contson"])').extract())
            # print('--> ', cont.xpath('div[@class="contson"]/text()').extract_first())
            # print(item)
            yield item
        page_link = response.xpath('//*[@id="FromPage"]/div/a[1]/@href').extract_first()
        if page_link is not None:
            next_page = self.domian + page_link
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)
