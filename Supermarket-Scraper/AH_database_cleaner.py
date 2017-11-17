# coding: utf-8

# In[ ]:

########################################################################## 
#
# Script to clean up product information database scraped from the AH 
# supermarket website.
#
# This script was created using the Jupyter notebook. It takes the 
# original output from scrapy and using post-processing the data is 
# cleaned and saved to a new .csv file for use in the next stage of
# interfacing with the data.
#
# Author: McGregor Drummond
# Date: 24 July 2017
# Finished: 25 July 2017
#
##########################################################################


# In[1]:

# import required modules
import csv
import pandas as pd
import numpy as np
import re


# In[2]:

db = pd.read_csv('ah-db.csv') #import scrapy .csv output

# inspect the data
#db.shape
#db.dtypes
db.head(5)


# In[3]:

# reorder the columns into required format
cols = list(db)

cols.insert(0, cols.pop(cols.index('Title')))
db = db.reindex(columns = cols)
cols = list(db)
db['Title'] = db['Title'].str.lower()

cols.insert(6, cols.pop(cols.index('Carbs')))
db = db.reindex(columns = cols)
cols = list(db)

cols.insert(6, cols.pop(cols.index('Fat')))
db = db.reindex(columns = cols)
cols = list(db)


# In[4]:

db['Weight_dummy'] = db['Weight'] # create dummy column containing only integers for later use

# start to remove all non-integer elements from dummy column
db['Weight_dummy'] = db['Weight_dummy'].str.replace('per stuk', '1').str.replace('per bosje', '1')

#chars = ['kg','ca.','ml','stuk','per','l',',','stuks','g','per stuk']
chars = ['k','g','c','a','.','m','l','s','t','u','k','p','e','r','l','b','o','j']
for ch in chars:
    db['Weight_dummy'] = db['Weight_dummy'].str.replace(ch, ' ')

db['Weight_dummy'] = db['Weight_dummy'].str.replace(',', '.')
db['Calories'] = db['Calories'].str.replace(',', '.')
db['Protein'] = db['Protein'].str.replace(',', '.')
db['Carbs'] = db['Carbs'].str.replace(',', '.')
db['Fat'] = db['Fat'].str.replace(',', '.')


# In[5]:

# final removal of non-integer elements
x_str_loc = db.index[db['Weight_dummy'].str.contains('x')==True] # find rows containing 'x'

# the 'x' represents a multiplication so here we go through row by row to make this calculation
for i in range(len(x_str_loc)):
    dummy = (db['Weight_dummy'][x_str_loc[i]].split()[::2])
    dummy = pd.to_numeric(dummy)
    db.set_value(x_str_loc[i],'Weight_dummy',dummy[0]*dummy[1])


# In[6]:

# check for NaN values and set it zero. These elements have been confirmed to be zero.
db['Calories'] = pd.to_numeric(db['Calories'],errors = 'coerce').fillna(0)
db['Protein'] = pd.to_numeric(db['Protein'],errors = 'coerce').fillna(0)
db['Carbs'] = pd.to_numeric(db['Carbs'],errors = 'coerce').fillna(0)
db['Fat'] = pd.to_numeric(db['Fat'],errors = 'coerce').fillna(0)
db['Weight_dummy'] = pd.to_numeric(db['Weight_dummy'],errors = 'coerce')
# Calories with no value can be calculated using the macronutrients
db['Calories'] = db['Calories'].replace(0,(db['Protein']+db['Carbs'])*4+db['Fat']*9)

NaNs = db[db.isnull().T.any().T]
NaNs # check if there are any remaining NaN values


# In[7]:

# Create new column for the price of each item per 100 g/ml/item to later calculate price of meals
db.loc[db['Weight'].str.contains('g'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'] / 100)
db.loc[db['Weight'].str.contains('kg'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'] * 10)
db.loc[db['Weight'].str.contains('l'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'] * 10)
db.loc[db['Weight'].str.contains('cl'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'] / 10)
db.loc[db['Weight'].str.contains('ml'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'] / 100)
db.loc[db['Weight'].str.contains('stuk'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'])
db.loc[db['Weight'].str.contains('bosje'), 'Price/100 (g/ml/stuk)'] = db['Price'] / (db['Weight_dummy'])

db['Price/100 (g/ml/stuk)'] = np.round(db['Price/100 (g/ml/stuk)'], 2) # round float to 2 decimal places

# reorder the columns again
cols = list(db)
cols.insert(3, cols.pop(cols.index('Price/100 (g/ml/stuk)')))
db = db.reindex(columns = cols)
cols = list(db)    


# In[8]:

# final check for NaN values in this new column
db['Price/100 (g/ml/stuk)'] = pd.to_numeric(db['Price/100 (g/ml/stuk)'],errors = 'coerce')

NaNs = db[db.isnull().T.any().T]
NaNs


# In[9]:

db = db.drop('Weight_dummy', 1) # drop the unneeded dummy column


# In[10]:

db.to_csv('./ah-db_sorted', index_label=False) # export new database to new .csv file
