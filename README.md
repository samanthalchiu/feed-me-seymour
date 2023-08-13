# feed-me-seymour

This is a content based recommendation system I made from scraping allrecipes.com. This recommendation system solely uses ingredients from each recipe in its algorithm. Naturally, the algorithm determines its recommendations from how  similar the ingredients are between recipes. 

scrapetime.py (recipes>spiders>scrapetime.py): scrapes data from allrecipes.com
dataprep_1.py: script that cleans irrelevant words from ingredient list
recs_2.py: script that conducts similarity matrix on recipes and outputs most similar recipes

recipes.csv (recipes>spiders>data>recipes.csv): table consisting of ingredients, ingredient IDs, and recipe website 
recipes_cleaned.csv (recipes>spiders>data>recipes_cleaned.csv): table consisting of ingredients, ingredient IDs, recipe website, recipename (ID number), and internal_list (list of ingredients without irrelevant words) 
