
########################################################################## 
#
# Second script to pull and save data for all international players from 
# www.dartsdatabase.co.uk in recent years.
#
# I ran Scrapy in a virtual environment (as recommended). To get this
# script working you will probably need to start a new project which 
# creates the items.py file and other neccessary components.
#
# Run from terminal with $ scrapy crawl dartmulti -o test.csv
# "dartmulti" = name of spider, "-o test.csv" writes our output
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
from darts.items import DartsIte

class Dart_single_Spider(scrapy.Spider): # open up the link to website and set some limitations
    name = "dartmulti"
    allowed_domains = ['www.dartsdatabase.co.uk']
    start_urls = ['http://www.dartsdatabase.co.uk/PlayerStats.aspx']
    BASE_URL = 'http://www.dartsdatabase.co.uk/'

    def start_requests(self): # create first list of urls for each player using first "10" pages of players in order of rank
        for i in xrange(10):
            url = 'http://www.dartsdatabase.co.uk/PlayerStats.aspx?statKey=1&pg=' + str(i+1) # cycle through the set number of pages
            yield FormRequest(url, callback=self.parse)

    def parse(self, response): # with link to player page, create new list of urls using first "10" pages of most recent results
        urls = []
        urls = response.xpath('//a/@href').extract() # extract the urls from the response data
        for url in urls: # cycle through the urls
            for i in xrange(10): # use only the first 10 pages of most recent results
                absolute_link = self.BASE_URL + url + '&organPd=All&tourns=All&plStat=2&pg='+ str(i+1) +'#PlayerResults' # create new url to follow
                yield FormRequest(absolute_link, callback=self.parse_player) 
  
    def parse_player(self, response): # Retrieve the required data
        player_name = response.xpath('//center/b/font/text()').extract() # extract the player name
  
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
