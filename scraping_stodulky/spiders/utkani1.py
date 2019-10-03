# -*- coding: utf-8 -*-
import scrapy
from scraping_stodulky.items import ScrapingStodulkyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import sys

class UtkaniSpider(scrapy.Spider):
    '''Spider downloading data for particular matches given in the start_urls
    list. From www.fotbalpraha.cz.
    '''
    name="utkani1"
    allowed_domains=["www.fotbalpraha.cz"]
    start_urls=['https://www.fotbalpraha.cz/zapas/13584-tj-sokol-stodulky-z-s-fk-loko-vltavin-z-s',
'https://www.fotbalpraha.cz/zapas/13701-tj-sokol-stodulky-z-s-afk-slavoj-podoli-praha-z-s',
'https://www.fotbalpraha.cz/zapas/14046-tj-sokol-stodulky-z-s-afk-slavia-malesice',
'https://www.fotbalpraha.cz/zapas/14274-fotbalovy-klub-cechie-dubec-z-s-tj-sokol-stodulky-z-s',
'https://www.fotbalpraha.cz/zapas/14460-tj-sokol-kralovice-z-s-tj-sokol-stodulky-z-s',
'https://www.fotbalpraha.cz/zapas/14628-afk-slavoj-podoli-praha-z-s-tj-sokol-stodulky-z-s',
'https://www.fotbalpraha.cz/zapas/14784-tj-sokol-stodulky-z-s-fk-dukla-praha',
'https://www.fotbalpraha.cz/zapas/14918-tj-sokol-stodulky-z-s-sk-aritma-praha-z-s',
'https://www.fotbalpraha.cz/zapas/14979-sportovni-klub-zbraslav-tj-sokol-stodulky-z-s'
]

    def parse(self, response):# jak se parsuje, musi existovat, aplikuje se na vsechny, takto musi u toho zakladniho spider byt definova
            vysledek_konec = response.xpath('//div[contains(@class, "game__scoreboard-score")]/text()').extract() #normalize-space v xpath maže mezery a řádky ve výsledném textu
            vysledek_polocas = response.css("div.game__scoreboard-score").css("span::text").extract()
            vysledek = vysledek_konec[0].strip() + " " + vysledek_polocas[0].strip()
            kiv = response.xpath('//div[contains(@class, "game__roster game__roster--top")]')
            sestava_domacich = kiv.css("div.game__roster-item").css("a::text").extract()[:11]
            sestava_d = ", ".join(sestava_domacich)           
            sestava_hoste = kiv.css("div.game__roster-item").css("a::text").extract()[11:]
            sestava_h = ", ".join(sestava_hoste)            
            nahradnici_domaci = response.css('div.game__roster')[1].css("div.col-12")[0].css("div.game__roster-item").css("a::text").extract()            
            nahradnici_d = ", ".join(nahradnici_domaci)
            nahradnici_hoste = response.css('div.game__roster')[1].css("div.col-12")[1].css("div.game__roster-item").css("a::text").extract()
            nahradnici_h = ", ".join(nahradnici_hoste)
            goly = response.xpath('//div[contains(@class, "table-responsive game__timeline")]').xpath('//i[contains(@class, "ico ico-goal")]/following-sibling::a[1]/text()').extract()
            sestava_sokol = response.css("div.game__scoreboard").css("span.long::text").extract_first()
            soutez = response.xpath('//div[contains(@class, "game__league")]//a/text()').extract()[0]
            kolo = response.xpath('//div[@class = "game__info"]//b/text()').extract()[0]
            index = kolo.find(".")
            kolo = kolo[:index]
            datum_cas = response.xpath('//div[@class = "game__info"]//b/text()').extract()[1:3]
            souper1 = response.css("div.game__scoreboard-team")[0].css("span.middle::text").extract()
            souper2 = response.css("div.game__scoreboard-team")[1].css("span.middle::text").extract()
            souperi = souper1[0] + " - " + souper2[0]
            listy = []
            listy2 = []
            for i in goly:
                if (i in sestava_domacich) or (i in nahradnici_d):
                    listy.append(i)
                else:
                    listy2.append(i)
            
            listy = ", ".join(listy)
            listy2 = ", ".join(listy2)
            if "Sokol Stod" in sestava_sokol:
                    if listy == []:
                        l = ItemLoader(item = ScrapingStodulkyItem(), response = response)
                        l.add_value("Soutez", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum",datum_cas)
                        l.add_value("Souperi", souperi)
                        l.add_value("Vysledek", vysledek)
                        l.add_value("Sestava", sestava_d)
                        l.add_value("Goly", "bez vstřeleného gólu")
                        l.add_value("Nahradnici", nahradnici_d)

                        return l.load_item()
                    else:
                        l = ItemLoader(item = ScrapingStodulkyItem(), response = response)
                        l.add_value("Soutez", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum",datum_cas)
                        l.add_value("Souperi", souperi)
                        l.add_value("Vysledek", vysledek)
                        l.add_value("Sestava", sestava_d)
                        l.add_value("Goly", listy)
                        l.add_value("Nahradnici", nahradnici_d)
                        
                        return l.load_item()
            else:
                    if listy2 == []:
                        l = ItemLoader(item = ScrapingStodulkyItem(), response = response)
                        l.add_value("Soutez", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum",datum_cas)
                        l.add_value("Souperi", souperi)
                        l.add_value("Vysledek", vysledek)
                        l.add_value("Sestava", sestava_h)
                        l.add_value("Goly", "bez vstřeleného gólu")
                        l.add_value("Nahradnici", nahradnici_h)
            
                        return l.load_item()
                    else:
                        l = ItemLoader(item = ScrapingStodulkyItem(), response = response)
                        l.add_value("Soutez", soutez)
                        l.add_value("Kolo",kolo)
                        l.add_value("Datum",datum_cas)
                        l.add_value("Souperi", souperi)
                        l.add_value("Vysledek", vysledek)
                        l.add_value("Sestava", sestava_h)
                        l.add_value("Goly", listy2)
                        l.add_value("Nahradnici", nahradnici_h)
            return l.load_item()