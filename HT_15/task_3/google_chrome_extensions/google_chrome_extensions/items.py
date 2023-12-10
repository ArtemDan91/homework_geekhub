import scrapy


class GoogleChromeExtensionsItem(scrapy.Item):
    extension_id = scrapy.Field()
    location = scrapy.Field()
    short_description = scrapy.Field()
    title = scrapy.Field()



