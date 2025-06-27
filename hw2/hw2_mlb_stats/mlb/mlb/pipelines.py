# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MlbPipeline:
    def process_item(self, item, spider):
        item['player'] = self.process_player(item['player'])
        return item
    def process_player(self, player_name):
        #用bs4找出姓與名
        #字串串接
        return player_name.strip()
