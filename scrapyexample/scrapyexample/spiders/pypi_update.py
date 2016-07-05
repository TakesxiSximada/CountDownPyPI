# -*- coding: utf-8 -*-
import logging
from functools import lru_cache

import feedparser
from scrapy.spiders import Spider

from ..items import ReleaseItem

logger = logging.getLogger(__name__)


class InvalidRecordError(Exception):
    pass


class Release:
    def __init__(self, record):
        """
        :param dict record: `record` must be have keys following.
        'title', 'summary', 'link'.
        """
        self._record = record

    def _get(self, key):
        try:
            return self._record[key]
        except KeyError as err:
            raise InvalidRecordError(
                '_record must be have keys following, title, summary, link.'
                ': {}'.format(err)
                )

    @property
    @lru_cache()
    def link(self):
        return self._get('link')

    @property
    @lru_cache()
    def summary(self):
        return self._get('summary')

    @property
    @lru_cache()
    def title(self):
        return self._get('title')

    @property
    @lru_cache()
    def name(self):
        return self.title.split()[0]

    @property
    @lru_cache()
    def version(self):
        try:
            return self.title.split()[1]
        except IndexError:
            logger.error('No version: %r', self._record['title'])
            return ''


class PypiUpdateSpider(Spider):
    name = "pypi.update"
    allowed_domains = ["pypi.python.org"]
    start_urls = (
        r'https://pypi.python.org/pypi?%3Aaction=rss',
    )

    def parse(self, response):
        feed = feedparser.parse(response.body)
        for record in feed.entries:
            release = Release(record)
            item = ReleaseItem()
            item['name'] = release.name
            item['version'] = release.version
            item['link'] = release.link
            item['summary'] = release.summary
            yield item
