# -*- coding: utf-8 -*-
from functools import lru_cache
import elasticsearch


class PackageElasticsearchDataStore:
    index = 'pypi_ranking'
    doc_type_package = 'package'
    doc_type_release = 'release'
    schema = {}

    def __init__(self, es):
        """
        :param elasticsearch.client.Elasticsearch es: Elasticsearch Client object
        """
        self.es = es

    def register(self, item):
        name = item['name']
        self.es.index(index=self.index, doc_type=self.doc_type_package, id=name, body={
            'name': name,
            })
        self.es.index(index=self.index, doc_type=self.doc_type_release, body={
            'name': name,
            'version': item['version'],
            'link': item['link'],
            'summary': item['summary'],
            })


@lru_cache()
def create_datastore(url):
    conn = elasticsearch.Elasticsearch(url)
    return PackageElasticsearchDataStore(conn)


class PyPIPackagePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=crawler.settings.get('ELASTICSEARCH_URL'),
            )

    def __init__(self, url):
        self.url = url

    def open_spider(self, spider):
        self.datastore = create_datastore(self.url)

    def process_item(self, item, spider):
        self.datastore.register(item)
