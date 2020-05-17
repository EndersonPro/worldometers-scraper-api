import os
from redis import Redis
import json

REDIS_HOST = os.getenv('REDIS_HOST') if not os.getenv('REDIS_HOST') == None else 'localhost'
REDIS_PORT = os.getenv('REDIS_PORT') if not os.getenv('REDIS_PORT') == None else '6379'
r = Redis(host=REDIS_HOST, port=REDIS_PORT)

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