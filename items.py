import scrapy


class TaobaoScrapyItem(scrapy.Item):
    shop_name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    shop_location = scrapy.Field()
    item_id = scrapy.Field()
    shop_url = scrapy.Field()
    item_url = scrapy.Field()
