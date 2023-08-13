# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    recipeinfo = scrapy.Field()
    ingredients = scrapy.Field()
    ingredientID = scrapy.Field()