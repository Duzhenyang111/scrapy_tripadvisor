# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter


class WangyiJobPipeline:
    def open_spider(self,spider):
        self.file = open('job.json','wb')
    # def __init__(self) -> None:
    #     self.file = open('job.json','wb')
    def process_item(self, item, spider):
        json_data = json.dumps(dict(item),ensure_ascii=False) + ',\n'
        self.file.write(json_data.encode('utf-8'))
        return item
    
    # def __del__(self):
    #     self.file.close()
    def close_spider(self,spider):
        self.file.close()
