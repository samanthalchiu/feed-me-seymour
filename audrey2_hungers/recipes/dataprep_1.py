# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:36:42 2023

@author: saman
"""
import os
import pandas as pd
import re
import numpy as np
#import matplotlib.pyplot as plt 
import collections
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def createingredientlist(df):
    pattern = r'(?<=[^\s]),(?=[^\s])'
    df['recipename'] = None
    for i in (df.index):  
        #get recipe name 
        # add in a check in which if the numel(curringredientID) does not match numel(curringredients), we toss that recipe and move forward 
        
        curringID = df.ingredientID[i].split(',')
        curring = re.split(pattern, df.ingredients[i])
        currrecipe = '/' + df.recipeinfo[i].split('/')[-3] + '/'
        repnum = len(df.ingredientID[i].split(','))
        if len(curringID) == len(curring):
            if i == 0:
                ingredientID = curringID
                ingredients = curring
                recipeID = [currrecipe] * repnum
            # get index of ingredient list that has spaces in it
            else:
                ingredientID = ingredientID + curringID
                ingredients = ingredients + curring
                recipeID = recipeID + [currrecipe] * repnum
            # if consecutive spaces, 
            df.recipename[i] = currrecipe
        else: 
            #compile list of indexes to drop from recipe list
            if 'idxToDrop' in locals():
                idxToDrop = np.append(idxToDrop,i)
            else:
                idxToDrop = np.array(i)
    new_df= pd.DataFrame(list(zip(ingredientID, ingredients, recipeID)),columns =['ingredientID', 'ingredient','recipeID'])
    
    return df, new_df, idxToDrop


def remove_words(s, patt):
    # compile a pattern to search for 'i', 'like', or 'and'
    # the word boundaries (\b) ensure that only whole words are matched
    pattern = re.compile(patt, re.IGNORECASE)

    # use the sub() method to replace all instances of the pattern with an empty string
    output = pattern.sub('', s)

    # replace multiple spaces with a single space and remove leading/trailing spaces
    output = re.sub(' +', ' ', output.strip())
    
    return output

def contains_letter(s):
    return any(c.isalpha() for c in s)

#%%
df_backup = pd.read_csv('C:\\Users\\saman\\OneDrive\\Documents\\recipes\\recipes\\spiders\\data\\recipes.csv')
df = df_backup
#ing_df = pd.read_csv('C:\\Users\\saman\\OneDrive\\Documents\\recipes\\recipes\\ingredients.csv')
#remove recipes that have a colon in there, heck that 
df = df.drop(df[df['ingredients'].str.contains(':', case=False)].index, inplace = False)

# let's maybe make this longform? 
#df["recipename"] = " "
output = createingredientlist(df)

idxToDel = output[2]
ing_df = output[1]
df = output[0]
#remove all recipes with errors 
df = df.drop(index = idxToDel)
#ing_df = ing_df.drop_duplicates(subset='ingredientID', keep="first")
del output

ingdf_backup = ing_df

#%% let's check out our data; 
# sort by df.ingredientID; get tally of how many IDs are associated with how many ingredients 

#ing_df= ing_df.drop_duplicates(subset=['ingredientID','ingredient'], keep="first").reset_index(drop = True)

#sorted_ing = ing_df.sort_values('ingredient')
#sorted_ID = ing_df.sort_values('ingredientID')

#%% if we can get words like "and", "into", "in", and "as" out of the ingredient_internal name, that would be ideal!!  

#remove ['and','into','in','as']
ing_df['internal_ing'] = [remove_words(x, r'\b(into |as |and |in )\b') for x in ing_df['ingredient']] 

#%% then we get rid of qualifier words; words that end in ed, en, -ces, -ess, -ly

#let's find our ingredient qualifiers; a lot of them are after commas within the ingredient itself 

qual_df = ing_df.loc[ing_df['internal_ing'].str.contains(',', case=False)]
# get the qualifiers from the ingredients 
qual_list = pd.DataFrame([x.split(',') for x in qual_df.internal_ing]) #, columns=['internal_ing', 'qualifier'])
#get list of qualifiers and their counts

qual_list = qual_list.melt(var_name='columns', value_name='index')
qual_list = qual_list[qual_list['columns'] > 0]
qual_summ = qual_list['index'].value_counts()

wordlist = [x.split(' ') for x in qual_summ.index]
wordlist = sum(wordlist, [])
count = pd.DataFrame(collections.Counter(wordlist).most_common())

ed_words = count.loc[count[0].str.contains('ed', case=True)]
ed_words = ed_words[-ed_words[0].str.contains('\(|\)|Cheddar |red |Red |seed')]

#removing en is also okay except for chicken, Chicken, Green; less than 16 can be removed; make sure not case sensitive 
en_words = count.loc[count[0].str.endswith("en")]

#all good, remove it all! 
ces_words = count.loc[count[0].str.endswith("ces")]
ess_words = count.loc[count[0].str.endswith("ess")]
ly_words = count.loc[count[0].str.endswith("ly")]
ly_words = ly_words[-ly_words[0].str.contains('\(|\)')]

stringsToRemove = ['inch', 'inches','cubes','cut']  # if a string CONTAINS the word inch or inches, cubes, or cut, remove it 

wordsToRemove = stringsToRemove + ed_words[0].tolist() + en_words[-en_words[0].str.contains('|'.join(['chicken', 'green']))][0].tolist() + ces_words[0].tolist() + ly_words[0].tolist() + ess_words[0].tolist()#,dash_words)
wTR = '\\b(' + '|'.join(wordsToRemove) + ')\\b'

ing_df['internal_ing'] = [remove_words(x, wTR) for x in ing_df['internal_ing']]

#%% let's fix up the ingredients list again

#now that we've removed a lot of words, we may need check if there are any trailing commas 
qual_df = ing_df[ing_df['internal_ing'].str.contains(',', case=False)]
# get the qualifiers from the ingredients 
qual_list = pd.DataFrame([x.split(',') for x in qual_df.internal_ing])
# for all the ingredients, make sure to remove the comma at the end of the string 
for x in qual_df.index:
    #split by commas; for all the actual text, recompile that into a new string and replace it 
    strtofix = qual_df.loc[x,'internal_ing'].split(',')
    strtofix = [x.strip() for x in strtofix if contains_letter(x)] # we have some leading spaces too we need to get rid of 
    ing_df.loc[x,'internal_ing'] = ', '.join([x for x in strtofix if x.strip()]) #we only combine text back together

#%% recompile recipes? screw the ingredient IDs 
recipenames = df.drop_duplicates(subset = ['recipename'], keep='first')
recipenames = recipenames['recipename'].tolist()

for r in recipenames:
# get ingredient associated with recipe 
    curring = ing_df[ing_df['recipeID'].str.contains(r)]
    curring = curring['internal_ing'].tolist()
# recompile such that a comma comes between each ingredient     
    if 'inglist' in locals(): 
        inglist = inglist + [','.join([x for x in curring])]
    else:
        inglist = [','.join([x for x in curring])]

df['internal_list'] = inglist

# internal check; we should start and end with the same # of ingredients!!! 
#%%

df.to_csv('C:\\Users\\saman\\OneDrive\\Documents\\recipes\\recipes\\spiders\\data\\recipes_cleaned.csv',sep=',')
# let's write this to a new csv file 