########################################################################## 
#
# Script to retrieve film details (genre etc.) and cast/crew from the 
# https://www.themoviedb.org/?language=en website.
#
# This script was created using the Jupyter notebook and converted to a 
# python text file to be run in the cmd. It cycles through each unique
# filmID and pulls the data from the webpage. A list of filmIDs is created
# using another script which required a lot of work to find unique matching
# titles between The Movie Database and The Boxoffice data.
#
# Author: McGregor Drummond
# Date/Finished: October 2017
#
##########################################################################


#Import all required libraries

import pandas as pd
import numpy as np
import csv
import json
import regex
import requests
import os

#DEFINE ALL FUNCTIONS FIRST

###########
def main(baseURL, apiKey, movieID, DIR, fname): #main function call to cycle through filmIDs
    
    
    URL = baseURL + str(movieID) + '?api_key=' + apiKey
    parsed = retrieveData(URL)
    writeToFile(parsed, DIR, fname)

###########
def retrieveData(url): #retrieve the json data
    
    
    data = requests.get(url).text
    dataParsed = json.loads(data)
    return dataParsed

###########
def writeToFile(dataParsed, DIR, fname): #save the data
    
    
    if not os.path.isfile(DIR+fname):
        with open(DIR + fname, 'w') as outFile:
            json.dump([], outFile)

	#due to json format the file must be reread every time you want to append data
	#more efficient to save all data in a list and write once but as the script only needed to be run once I just did it this way
    with open(DIR + fname) as inFile: 
        feed = json.load(inFile)
        feed.append(dataParsed)
    
        with open(DIR + fname, 'w') as outFile:
            json.dump(feed, outFile)


#####Input data#######

#first read in the filmID list 
DIR = 'C:/Users/Student/Downloads/Datasets/TheMovieDatabase/' #data location
fname = 'linkedIdTitle.xlsx'
df = pd.read_excel(DIR + fname, sheet_name= 'Sheet1')
idList = df.id.unique()

#extra input data
fname = 'MdbIDenBOtitel.json'
baseurl = 'https://api.themoviedb.org/3/movie/'
APIKEY = '###' #get personal API key from https://www.themoviedb.org/documentation/api?language=en

############# various base urls

#https://api.themoviedb.org/3/movie/{movie_id}?api_key=###APIKEY###&language=en-US #details
#https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=###APIKEY### #cast/crew

#############

for MOVIEID in idList: #cycle through list and call main function


    try:
        main(baseurl, APIKEY, MOVIEID, DIR, fname)
    except:
        print('Error occured with id: %s.' % (MOVIEID))

