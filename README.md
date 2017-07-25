# Supermarket-Scraper
- Project start date: 18 July 2017
- Single product script uploaded/working: 22 July 2017
- Full supermarket database: 24 July 2017
- Database cleaner script: 25 july 2017
# 

This project is geared towards learning how to scrape data from a website. I chose the [Albert Heijn](https://www.ah.nl/producten) website as we shop there and it will be useful to quickly compare prices and nutritional information of the products. This has been a steep learning curve as I began self-learning Python at the start of July but perseverance has paid off.

As the website uses javascript it took a while to find out how the data can be pulled. I ended up using [Scrapy](https://scrapy.org/) spiders to access the url and eventually found the link used to retrieve the data (in json format) from somewhere else. 

To begin with I focused on a single product to get the code up and running which then saves the data to .csv for later processing. I will then build upon this script to eventually retrieve all product information. Once all information as been scraped the information will be used to create meal plans in which the nutritional information and price can be determined. This may be eventually created in the form of a GUI.

For anyone reading this, if you have any suggestions as to how I can improve the code then please don't hesitate to get in touch!

Cheers.
