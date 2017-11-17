########################################################################## 
#
# First script to pull and save data of a single player from 
# www.dartsdatabase.co.uk
#
# I ran Scrapy in a virtual environment (as recommended). To get this
# script working you will probably need to start a new project which 
# creates the items.py file and other neccessary components.
#
# Run from terminal with $ scrapy crawl dartplayer -o test.csv
# "dartplayer" = name of spider, "-o test.csv" writes our output
#
# Author: McGregor Drummond
# Date: 31 July 2017
# Working: 31 July 2017
#
##########################################################################

# import required modules
import scrapy
from scrapy.http import FormRequest
import json
from darts.items import DartsItem

class Dart_single_Spider(scrapy.Spider):
    name = "dartplayer" # name of spider
    allowed_domains = ['http://www.dartsdatabase.co.uk']
    #first player data to scrape
    start_urls = ['http://www.dartsdatabase.co.uk/PlayerDetails.aspx?PlayerKey=6487&organPd=All&tourns=All&plStat=2#PlayerResults']#'http://www.dartsdatabase.co.uk/PlayerDetails.aspx?PlayerKey=1395&organPd=All&tourns=All&plStat=2#PlayerResults']
        
    def parse(self, response):
        player_name = response.xpath('//center/b/font/text()').extract() # extract the player name

        # used to write received data to file for initial inspection
        #filename = 'darts.html' 
        #with open(filename, 'wb') as f:
        #    f.write(response.body)

        # after inspection and experimentation I found the table with the data I wanted
        table = response.xpath('//table/tr/*/*/text()|//table/tr/td/text()').extract()
        start_index = table.index('Score') # create the start point/element for our required data

        # cycle through the saved table and save the required data to respective array
        date = table[start_index+1:-2:7] #date
        tour = table[start_index+2:-2:7] #tournament
        cate = table[start_index+3:-2:7] #category
        roun = table[start_index+4:-2:7] #round
        resu = table[start_index+5:-2:7] #result
        oppo = table[start_index+6:-2:7] #opponent
        scor = table[start_index+7:-2:7] #score


        item = DartsItem() # call on our function inside items.py
        
        # assign the saved strings/values from the arrays to their respective fields        
        for i in xrange(len(date)):
            item['Date'] = date[i]
            item['Tournament'] = tour[i]
            item['Category'] = cate[i]
            item['Round'] = roun[i]
            item['Result'] = resu[i]
            item['Opponent'] = oppo[i]
            item['Score'] = scor[i]
            item['Player'] = player_name
            yield item
            
