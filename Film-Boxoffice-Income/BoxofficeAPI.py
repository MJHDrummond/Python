########################################################################## 
#
# Script to retrieve film boxoffice income from the http://boxofficenl.net/
# website.
#
# This script was created using the Jupyter notebook and converted to a 
# python text file to be run in the cmd. It cycles through each webpage
# using month/year constraints and extracts the required data from the
# table embedded on the website.
#
# Author: McGregor Drummond
# Date/Finished: October 2017
#
##########################################################################


#Import all required libraries

import requests
import csv
from bs4 import BeautifulSoup as bs
import re
import os

#DEFINE ALL FUNCTIONS FIRST

###########
def main(baseUrl, wk, yr): #main function call to cycle through webpages
    
    
    URL = baseUrl + str(yr) + '&wk=' + str(wk)
    htmlData = retrieveData(URL)
    cleanData, csvHeaders = dataCleaner(htmlData, wk, yr)
    writeToFile(csvHeaders, cleanData, DIR, fname)
    print('Data written for week: %s and year: %s.' % (wk, yr))

###########
def retrieveData(url): #retrieve html page as text
    
    
    data = requests.get(url).text
    soup = bs(data, 'html5lib')
    return soup

###########
def dataCleaner(soupInput, wk, yr): #clean the html text 
    
    
    cleanHeaders = []
    cleanBox = []
    soup = soupInput
    
	#extract and create list of table/column headers
    headersList = [str(item).lower().replace('\t','') for item in soup.find_all('th')] #remove tags
    for i in range(len(headersList)): 
        cleanHeaders.append(''.join(list(re.sub("<.*?>", "", (headersList[i])))))
    cleanHeaders.extend(['week', 'jaar'])

	#extract the actual table information/data
    boxList = [str(item).lower() for item in soup.find_all('td')]
    for i in range(len(boxList)):
        cleanBox.append(''.join(list(re.sub("<.*?>", "", (boxList[i])))))

    cleanerBox = cleanBox[:-2 or None] #remove last 2 unneeded elements
    for i in range(len(cleanerBox),-1,-(len(cleanHeaders)-2)): #add week column
        cleanerBox.insert(i, str(wk))
    cleanerBox.pop(0) #remove first element

    for i in range(len(cleanerBox),-1,-(len(cleanHeaders)-1)): #add year column
        cleanerBox.insert(i, str(yr))
    cleanerBox.pop(0) #remove first element
    
    #remove 'the' column from data as this column is only added after 2016
    if len(cleanHeaders) > 12:
        for i in range(len(cleanerBox)-7, 0, -len(cleanHeaders)): 
            cleanerBox.pop(i) #remove each 'the' element
        cleanHeaders.pop(6) #remove the column header

    return cleanerBox, cleanHeaders

###########
def writeToFile(headers, data, directory, filename): #save the extracted data
    
    
    cleanHeaders = headers
    cleanerBox = data
 
    with open(directory + filename, 'a+') as csvfile:
        csvfile.seek(0) #jump to start of file
        writer = csv.writer(csvfile)
        try :
            header = next(csv.reader(csvfile)) #header found
        except StopIteration :  #no header found
            writer.writerow(cleanHeaders)
        
        csvfile.seek(0,2) #jump to end of file    
        try : 
            for i in range(int(len(cleanerBox)/len(cleanHeaders))):
                writer.writerow(cleanerBox[i*len(cleanHeaders):(i+1)*len(cleanHeaders)])
        except ValueError : 
            print('Error has occurred')


#####Input data#######

DIR = '###' #save data to this directory ex. 'C:/Users/Student/Downloads/Datasets/Boxoffice/'
fname = 'boxoffice.csv'

baseURL = 'http://www.boxofficenl.net/boxoffice.asp?jr='

yearList = range(2017,2002,-1) #data starts from 2003
weekList = range(53,0,-1) #some years have 53 weeks in ISO dating


# Call the main loop inside for loops around week and year
for year in yearList:
    for week in weekList:
        try:
            main(baseURL, week, year)
        except:
            print('Error occured at week: %s and year: %s.' % (week, year))

