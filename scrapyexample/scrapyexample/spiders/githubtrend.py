# -*- coding: utf-8 -*-
import scrapy


class GithubtrendSpider(scrapy.Spider):
    name = "githubtrend"
    allowed_domains = ["https://github.com/trending"]
    start_urls = (
        'https://github.com/trending/',
    )

    def parse(self, response):
        print(response)
