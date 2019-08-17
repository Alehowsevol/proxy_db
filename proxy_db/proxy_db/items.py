import scrapy


class ProxyDbItem(scrapy.Item):
    ip_address = scrapy.Field()
    port = scrapy.Field()

