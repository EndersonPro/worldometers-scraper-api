from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, jsonify, request
from scrapper import Scrapper
import resolvers as r
from redis import Redis
import rx
from rx import operators as ops
import json

app = Flask(__name__)

o = rx.interval(1.0)
sub = o.subscribe(lambda value: print("El valor es {}".format(value)))

r = Redis(host='localhost', port='6379')

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200
    
@app.route('/graphql', methods=['POST'])
def graphql_server():
    sub = o.subscribe(lambda value: print("El valor es {}".format(value)))

    type_defs = load_schema_from_path('schema.graphql')

    query = QueryType()
    continent = ObjectType('Continent')
    country = ObjectType('Country')

    query.set_field('continents', r.continents_resolver)
    query.set_field('countries', r.countries_resolver)
    query.set_field('country_by_name', r.country_by_name_resolver)
    query.set_field('continent_by_name_resolver', r.continent_by_name_resolver)

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
        sub = o.subscribe(lambda value: print("El valor es {}".format(value)))
        co = json.loads(r.get('countries'))
        cs = json.loads(r.get('continents'))
        totalr = json.loads(r.get('total'))
        return jsonify({ 'data': { 'countries': co, 'continents': cs, 'total': totalr }})
    except:
        sub.unsubscribe()
        return jsonify({ 'data': '', 'message': 'An error ocurred.' })

def update_data_redis():
    s = Scrapper()
    countries, continent = s.scrapping()    
    r.set('countries', json.dumps(countries))
    r.set('continents', json.dumps(continent))
    r.set('total', json.dumps(len(countries) + len(continent)))

if __name__ == '__main__':
    update_data_redis()
    # app.run(host='0.0.0.0', port=80)
    app.run()


# test = rx.interval(1000000)
# test.subscribe(lambda value: print('Me estoy ejecutando cada 1 segundo {}'.format(value)))