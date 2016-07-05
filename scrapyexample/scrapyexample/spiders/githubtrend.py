# -*- coding: utf-8 -*-
import scrapy


class GithubtrendSpider(scrapy.Spider):
    name = "githubtrend"
    allowed_domains = ["github.com"]
    start_urls = (
        'https://github.com/trending/',
    )

    def parse(self, response):
        import ipdb; ipdb.set_trace()
        print(response)
