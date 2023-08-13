# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:36:38 2023

@author: saman
"""

import os
import pandas as pd
#import re
import numpy as np
import matplotlib.pyplot as plt 
#import collections
#from difflib import SequenceMatcher
#from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
#from scipy.spatial import distance_matrix
from scipy.cluster.hierarchy import dendrogram, linkage


#%% okay time to try this 
df = pd.read_csv('C:\\Users\\saman\\OneDrive\\Documents\\recipes\\recipes\\spiders\\data\\recipes_cleaned.csv')

getrecipename = [x.split('/')[-2] for x in df['recipeinfo']]

df['recipename_short'] = getrecipename
# gonna remove recipes that only have 1 ingredient in it 
df = df.loc[df['internal_list'].str.contains(',')]
df = df.reset_index(drop=True)

#these are all the recipes with just one ingredient
#testdf = df.drop(df[df['internal_list'].str.contains(',')].index)

# need to find similarity between two vectors of ingredients
ingbyrecipe = [x for x in df['internal_list']]

#bkup_ingbyrecipe = ingbyrecipe
#ingbyrecipe = ingbyrecipe[0:10]

# first need the tf-idf
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(ingbyrecipe)

# get features 
feature_names = vectorizer.get_feature_names_out()
# Compute the cosine similarity matrix
similarity_matrix = cosine_similarity(X)
#%%
#now that we have a similarity matrix for all recipes, let's ping it..? 

#get rand index of recipes 
recidx = np.random.choice(len(ingbyrecipe),750)
# for each recipe
recinfo = df.loc[recidx]
recinfo = recinfo[['recipename_short','internal_list']]

# get top 10 recipes' index 
allidx = [(-similarity_matrix[r]).argsort()[1:11] for r in recidx] # sort descending order 
# then get their corresponding scores 
allscores = [similarity_matrix[recidx[r]][allidx[r]] for r in range(len(recidx))] #
# and their recipename and ingredient list 
allrecs = [df.loc[allidx[r]] for r in range(len(recidx))]

#reshape the output so i can write it to a file 
recscorecol = [allscores[a][b] for a in range(len(allscores)) for b in range(len(allscores[a]))]
recIDcol = [allrecs[a].iloc[b]['recipename_short'] for a in range(len(allrecs)) for b in range(len(allrecs[a]))]
recingcol = [allrecs[a].iloc[b]['internal_list'] for a in range(len(allrecs)) for b in range(len(allrecs[a]))]
IDcol = [recinfo.iloc[a]['recipename_short'] for a in range(len(allrecs)) for b in range(len(allrecs[a]))]
ingcol = [recinfo.iloc[a]['internal_list'] for a in range(len(allrecs)) for b in range(len(allrecs[a]))]


output = pd.DataFrame(list(zip(IDcol,ingcol,recIDcol,recingcol,recscorecol)),columns =['currID', 'curring','recID','rec_ing','rec_score'])

output.to_csv('C:\\Users\\saman\\OneDrive\\Documents\\recipes\\recipes\\spiders\\data\\output.csv',sep=',')


#%%

# new ideas:
    # some recipes have 1 ingredient in them; remove!! 
    # some recipes are ingredients for other recipes; what to do with these? likely fine? just need to think about it! 
    # do a clustering analysis to get cuisine/dish type from recipe clusters 
        ## are there recipe clusters to use? hopefully! 
        ## this is probably a representation of the data i have and not necessarily anything useful...? but if i could extract some of it, that'd be cool! 
            ### would i want actual cuisine type? not all dishes have a cuisine type though?? we'll see! 
        ## we are assuming that cuisines have unique ingredients (but cuisines like indian food vs japanese vs chinese all use rice, but not all have raw fish or masala powder or something)
            ## this is exploratory! 
    # so the tfidf is getting that two recipes are similar by comparing exact strings, but what about similar ingredients? 
    # i should be recommended things with chicken if i have a beef dish. how can i get tfidfs of the ingredients themselves? can i? what is best way to do?

#%% ezploratory clustering analysis: all my clusters have found strange things; some clusters too large, some too small... will work on this one day.
## goal: use ingredients to extract meal categories and/or cuisine; hopefully an ingredient like fish sauce will cluster some recipes together and i can label that vietnamese food 

sampleclusteridx = np.random.choice(len(ingbyrecipe),750)

sampledf = df.loc[sampleclusteridx]
sampledf = sampledf.reset_index(drop=True)

ingbyrecipe = [x for x in sampledf['internal_list']]

X = vectorizer.fit_transform(ingbyrecipe)

# get features 
feature_names = vectorizer.get_feature_names_out()
# Compute the cosine similarity matrix
similarity_matrix = cosine_similarity(X)

distance_matrix = 1 - similarity_matrix
desired_number_of_clusters = 20;
clustering = AgglomerativeClustering(n_clusters=desired_number_of_clusters, metric='precomputed', linkage='average')
cluster_labels = clustering.fit_predict(distance_matrix)

# Using linkage to get hierarchical structure
linked = linkage(distance_matrix, 'average')

# Plotting dendrogram
plt.figure(figsize=(10, 7))
dendrogram(linked, no_labels=True)
plt.show()

clusters = {}

recipelist = df['recipename_short'].tolist()

for recipelist, label in zip(recipelist, cluster_labels):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(recipelist)

clustersize = [len(clusters[x]) for x in range(len(clusters))]


# Now you can access items in each cluster using the 'clusters' dictionary
for label, items_in_cluster in clusters.items():
    print(f"Cluster {label}:")
    for item in items_in_cluster:
        print(item)
    print("\n")



