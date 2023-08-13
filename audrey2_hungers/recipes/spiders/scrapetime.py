import scrapy
from recipes.items import RecipesItem
from scrapy.spiders import SitemapSpider
from scrapy.linkextractors import LinkExtractor
class ScrapetimeSpider(SitemapSpider):
    name = 'scrapetime'
    allowed_domains = ['allrecipes.com']
    sitemap_urls = ['https://www.allrecipes.com/sitemap_2.xml']
    sitemap_rules = [
        ('/recipe/', 'parse')
    ]
    def parse(self, response):
        
        # first, check if that website actually HAS a recipe with it 
        
        # find "mntl-lrs-ingredients*"
        data = RecipesItem()
        # get recipe name from the link itself (allrecipes.com/recipe/*/*/; that second star)
        data["recipeinfo"] = response.xpath('//link[@rel="canonical"]/@href').get()
        
        
        # how to get cuisine: under "loc article-header", pull "mntl-text-link_2-0-*
        # we can parse the cuisine label from that 
        #data["category"] = 
        # ingredient list
        #### under "mntl-structured-ingredients__list"
        #### get each "data-ingredient-name"
        
        # ingredientlist = response.xpath('//span[@data-ingredient-name="true"]/text()').getall()
        # main_ingredients = []
        # for ingredient in ingredientlist:
            
        #     main_ingredient = ingredient.split(",")[0] if "," in ingredient else ingredient
        #     main_ingredients.append(main_ingredient.strip())
        #     #main_ingredient = ingredient.split(",")[0]
        #     #main_ingredients.append(main_ingredient)
        
        # data["ingredients"] = main_ingredients
        
        # i can already tell i need to remove the comma after ingredients with commas at the end 
        
        data["ingredients"] = response.xpath('//span[@data-ingredient-name="true"]/text()').getall()
        
        # also keep track of data-id, i wanna see if each ingredient has a unique data-id
        data["ingredientID"] = response.xpath('//li/@data-id').getall()
        return data


