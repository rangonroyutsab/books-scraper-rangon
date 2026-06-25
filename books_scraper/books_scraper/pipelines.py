# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CleanDataPipeline:
    def process_item(self, item, spider):
        item["title"] = item["title"].strip()
        item["price"] = (
            item["price"].strip().replace("£", "")
        )  #  will add more filter logics later
        item["availability"] = item["availability"].strip()
        item["category"] = item["availability"].strip()
        return item
