########################################################################## 
#
# First script to pull and save data of a single product from the Albert
# Heijn supermarket website.
#
# I ran Scrapy in a virtual environment (as recommended). To get this
# script working you will probably need to start a new project which 
# creates the items.py file and other neccessary components.
#
# Run from terminal with $ scrapy crawl items -o test.csv
# "items" = name of spider, "-o test.csv" writes our output
#
# Author: McGregor Drummond
# Date: 18 July 2017
# Working: 22 July 2017
#
##########################################################################

# import required modules
import scrapy
from scrapy.http import FormRequest
import json
from albert.items import AlbertItem

class ItemsSpider(scrapy.Spider):
    name = "items" # name of spider
    allowed_domains = ['www.ah.nl']
    start_urls = ['https://www.ah.nl/producten/product/wi30591/ah-kalkoenfilet'] # first product to test

    def parse(self, response):
        # receive response from start url but we don't do anything with it.
        url = 'https://www.ah.nl/service/rest/delegate?url=%2Fproducten%2Fproduct%2Fwi30591%2Fah-kalkoenfilet&_=1500537232483'
        return FormRequest(url, callback=self.parse_product_info)
        
    def parse_product_info(self, response):
        jsonresponse = json.loads(response.text) # save data from url response 
        
        # used to write received data to file for initial inspection
        #item_name = 'Kalkoenfilet'
        #filename = 'ah_db-%s.json' % item_name
        #with open(filename, 'wb') as f:
        #    f.write(json.dumps(jsonresponse, indent=4, sort_keys=True))

        # after inspection I found the table with the data I wanted. Not sure if there is a better/more efficient way to access the nested information...
        table = jsonresponse.get('_embedded').get('lanes')[8].get('_embedded').get('items')[0].get('_embedded').get('sections')[0].get('_embedded').get('content')[2].get('text').get('body').replace('th', ' ').replace('tr',' ').replace('td', ' ').replace('\\',' ').replace('/',' ').replace('[', ' ').replace(']', ' ').replace(')',' ').replace('(',' ').split()
        
        headers = ['Energie', 'Eiwitten', 'Koolhydraten', 'Vet'] # nutritional headers inside table
        headers_eng = ['Calories', 'Protein', 'Carbs', 'Fat'] # nutritional headers in English
        header_iloc = []
        for i in range(len(headers)): # find and save iloc of headers inside table
            header_iloc.append(table.index(headers[i]))

        item = AlbertItem() # call on our function inside items.py
        
        # find the strings/values and assign them to their respective fields
        item['Title'] = jsonresponse.get('title').split()[1]
        item['Weight'] = jsonresponse.get('title').split()[3]
        
        for i in range(len(headers)): # loop around headers to create nutrient fields
            item[headers_eng[i]] = table[header_iloc[i]+1] 
       
        item['Calories'] = table[header_iloc[0]+3] 

        yield item

# Example .csv output (any suggestions as to why the title order is wrong please let me know!)
# Carbs,Weight,Title,Calories,Fat,Protein
# 0,200,Kalkoenfilet,470,1,25
