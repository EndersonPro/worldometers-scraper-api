from scrapper import Scrapper

def continents_resolver(_, info):
    s = Scrapper()
    countries, continent = s.scrapping()
    return continent

def countries_resolver(_, info):
    s = Scrapper()
    countries, continent = s.scrapping()
    return countries