from redis import Redis
import json

r = Redis(host='localhost', port='6379')

def continents_resolver(_, info):
    cs = list(json.loads(r.get('continents')))
    return cs

def countries_resolver(_, info):
    co = list(json.loads(r.get('countries')))
    return co

def country_by_name_resolver(_, info, country):
    co = json.loads(r.get('countries'))
    return list(filter(lambda e: e.get('country') == country, co))[0]

def continent_by_name_resolver(_, info, country):
    cs = json.loads(r.get('continents'))
    return list(filter(lambda e: e.get('country') == country, cs))[0]