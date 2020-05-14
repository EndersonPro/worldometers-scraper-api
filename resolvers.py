from scrapper import Scrapper

def continents_resolver(_, info):
    s = Scrapper()
    countries, continent = s.scrapping()
    return continent

def countries_resolver(_, info):
    s = Scrapper()
    countries, continent = s.scrapping()
    return countries

def country_by_name_resolver(_, info, country):
    s = Scrapper()
    countries, continent = s.scrapping()
    return list(filter(lambda e: e.get('country') == country, countries))[0]

def continent_by_name_resolver(_, info, country):
    s = Scrapper()
    countries, continent = s.scrapping()
    return list(filter(lambda e: e.get('country') == country, countries))[0]