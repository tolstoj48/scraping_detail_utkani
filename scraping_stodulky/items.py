# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field



class ScrapingStodulkyItem(Item):
    Soutez=Field()
    Kolo=Field()
    Datum=Field()
    Souperi=Field()
    Vysledek=Field()
    Sestava=Field()
    Goly=Field()
    Nahradnici=Field()
    
