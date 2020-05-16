from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, jsonify, request
from scraper import Scraper
import resolvers as resolver
from redis import Redis
import rx
from rx import operators as ops
import json

app = Flask(__name__)

# Creating a subscriber to get the information every 5 minutes
o = rx.interval(300)
sub = o.subscribe(lambda _: update_data_redis())

# Redis instance
r = Redis(host='localhost', port='6379')

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200
    
@app.route('/graphql', methods=['POST'])
def graphql_server():
    type_defs = load_schema_from_path('schema.graphql')

    query = QueryType()
    continent = ObjectType('Continent')
    country = ObjectType('Country')

    query.set_field('continents', resolver.continents_resolver)
    query.set_field('countries', resolver.countries_resolver)
    query.set_field('country_by_name', resolver.country_by_name_resolver)
    query.set_field('continent_by_name_resolver', resolver.continent_by_name_resolver)

    schema = make_executable_schema(type_defs, [continent, country, query])

    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route('/api')
def index():
    try:
        co = json.loads(r.get('countries'))
        cs = json.loads(r.get('continents'))
        totalr = json.loads(r.get('total'))
        return jsonify({ 'data': { 'countries': co, 'continents': cs, 'total': totalr }})
    except:
        sub.unsubscribe()
        return jsonify({ 'data': '', 'message': 'An error ocurred.' })

def update_data_redis():
    s = Scraper()
    countries, continent = s.scraping()    
    r.set('countries', json.dumps(countries))
    r.set('continents', json.dumps(continent))
    r.set('total', json.dumps(len(countries) + len(continent)))

if __name__ == '__main__':
    update_data_redis()
    # app.run(host='0.0.0.0', port=80)
    app.run()