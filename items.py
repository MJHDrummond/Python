# -*- coding: utf-8 -*-
########################################################################## 
#
# Created by starting a new Scrapy project
#
##########################################################################

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AlbertItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Weight = scrapy.Field()
    Calories = scrapy.Field()
    Protein = scrapy.Field()
    Carbs = scrapy.Field()
    Fat = scrapy.Field()
    pass
