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

class DartsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Date = scrapy.Field()
    Tournament = scrapy.Field()
    Category = scrapy.Field()
    Round = scrapy.Field()
    Result = scrapy.Field()
    Opponent = scrapy.Field()
    Score = scrapy.Field()
    Player = scrapy.Field()
    pass
