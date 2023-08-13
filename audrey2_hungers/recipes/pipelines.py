# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


#class RecipesPipeline:
    #def process_item(self, item, spider):
        #return item
        #### data structure: long form? 
            ## each recipe has a cuisine tag with x rows for each ingredient
            
            ## maybe each ingredient can have a cuisine tagged to it? maybe! 