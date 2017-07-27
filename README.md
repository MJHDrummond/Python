# Supermarket-Scraper
- Project start date: 18 July 2017
- Single product script uploaded/working: 22 July 2017
- Full supermarket database: 24 July 2017
- Database cleaner script: 25 july 2017
- Meal plan script:
# 

This project is geared towards learning how to scrape data from a website. I chose the [Albert Heijn](https://www.ah.nl/producten) website as we shop there and it will be useful to quickly compare prices and nutritional information of the products. This has been a steep learning curve as I began self-learning Python at the start of July but perseverance has paid off.

As the website uses javascript it took a while to find out how the data can be pulled. I ended up using [Scrapy](https://scrapy.org/) spiders to access the url and eventually found the link required to retrieve the product data (in json format). 

To begin with I focused on a single product to get the code up and running. The data is then saved to .csv for later processing. I then expanded this this script to eventually retrieve all product information, again another steep learning curve. Once all information had been scraped it will be used to create meal plans in which the nutritional information and price can be determined. This goal is to eventually create a GUI for this process.

To the readers, if you have any suggestions as to how I can improve the code then please don't hesitate to get in touch!

Cheers.
