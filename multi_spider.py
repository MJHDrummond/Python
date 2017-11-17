########################################################################## 
#
# Second script to pull and save data of all required products from the 
# Albert Heijn supermarket website.
#
# I ran Scrapy in a virtual environment (as recommended). To get this
# script working you will probably need to start a new project which 
# creates the items.py file and other neccessary components.
#
# Run from terminal with $ scrapy crawl multi -o test.csv
# "items" = name of spider, "-o test.csv" writes our output.
#
# The .csv can now be pre-proccessed to search for required information.
#
# Author: McGregor Drummond
# Date: 22 July 2017
# Working: 24 July 2017
#
##########################################################################

# import required modules
import scrapy
import json
#import re

from scrapy.http import FormRequest
from albert.items import AlbertItem

class MultiSpider(scrapy.Spider):
    name = "multi" # name of spider
    allowed_domains = ['www.ah.nl']
    start_url = ['https://www.ah.nl/producten'] 
    BASE_URL = 'https://www.ah.nl/service/rest/delegate?url=' # base url used for creating links

    def start_requests(self): # create the connection
        url = 'https://www.ah.nl/service/rest/delegate?url=%2Fproducten&_=*?'
        yield FormRequest(url, callback=self.parse1)

    def parse1(self, response):
        jsonresponse = json.loads(response.text)
        links1 = [] # create empty list for new links found

        for i in range(7): # Change for how many categories to scrape in relation to website order
            # from original json url find and save links to the product categories
            links1.append(jsonresponse.get('_embedded').get('lanes')[0].get('_embedded').get('items')[i].get('navItem').get('link').get('href'))

        for link in links1: # create new links to take us closer to the product information
            absolute_link1 = self.BASE_URL + link.replace('/', '%2F') + '&_=*?'
            yield FormRequest(absolute_link1, callback=self.parse2)

    def parse2(self, response):
        jsonresponse = json.loads(response.text)
        links2 = [] # create new list for last set of links

        for i in range(100):
            for j in range(100):
                # new links aren't always in same location hence try is required here.
                try:
                    # save new links to list
                    links2.append(jsonresponse.get('_embedded').get('lanes')[i].get('_embedded').get('items')[j].get('navItem').get('link').get('href'))
                # if we look for a link in the wrong place we pass the error in order to continue searching
                except Exception:
                    pass
                    
        for link in links2: # create the next set of links to the product information
            absolute_link2 = self.BASE_URL + link.replace('/', '%2F') + '&_=1500879677612'
            # we have a lot of unneccessary links so this if statement makes sure we only forward on the important ones
            if 'producten%2Fproduct' in absolute_link2: 
                yield FormRequest(absolute_link2, callback=self.parse_product_info)

    def parse_product_info(self, response):
        jsonresponse = json.loads(response.text)

        headers = ['Energie', 'Eiwitten', 'Koolhydraten', 'Vet'] # nutritional headers we will search for in the table
        headers_eng = ['Calories', 'Protein', 'Carbs', 'Fat'] # nutritional headers in English
        header_iloc = []
        
        # the nutritional information is not always in the same location thus the nested loops are required to search for them
        for i in range(25):
            for j in range(10):
                try: # again using the try statement to skip over failed searches
                    table_dummy = jsonresponse.get('_embedded').get('lanes')[i].get('_embedded').get('items')[j].get('_embedded').get('sections')[0].get('_embedded').get('content')[2].get('text').get('body').replace('th', ' ').replace('tr',' ').replace('td', ' ').replace('\\',' ').replace('/',' ').replace('[', ' ').replace(']', ' ').replace(')',' ').replace('(',' ').split()
                    
                    # we need an if here as there were some false readings when searching for the table
                    # we make sure that it is indeed the table that was found by checking the first string element
                    if table_dummy[0] == 'table':
                        table = table_dummy
                        for k in range(len(headers)): # find and save iloc of headers inside the saved table
                            header_iloc.append(table.index(headers[k]))  

                        item = AlbertItem() # call on our function inside items.py
                        item['Title'] = jsonresponse.get('_embedded').get('lanes')[4].get('_embedded').get('items')[0].get('_embedded').get('product').get('images')[0].get('title')
                        item['Weight'] = jsonresponse.get('_embedded').get('lanes')[4].get('_embedded').get('items')[0].get('_embedded').get('product').get('unitSize')#.split()[-2]
                        item['Price'] = jsonresponse.get('_embedded').get('lanes')[4].get('_embedded').get('items')[0].get('_embedded').get('product').get('priceLabel').get('now')

                        for ii in range(len(headers)): # loop around headers to create nutrient fields
                            item[headers_eng[ii]] = table[header_iloc[ii]+1]

                        item['Calories'] = table[header_iloc[0]+3]

                        yield item 

                except Exception:
                    pass
                    
                    
