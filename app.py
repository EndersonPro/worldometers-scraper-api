from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, jsonify, request
from scrapper import Scrapper
import resolvers as r

app = Flask(__name__)

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200
    
@app.route('/graphql', methods=['POST'])
def graphql_server():

    type_defs = load_schema_from_path('schema.graphql')

    query = QueryType()
    continent = ObjectType('Continent')
    countries = ObjectType('Countries')

    query.set_field('continents', r.continents_resolver)
    query.set_field('countries', r.countries_resolver)


    schema = make_executable_schema(type_defs, [continent, countries, query])

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
    s = Scrapper()
    countries, continent = s.scrapping()
    total = len(countries) + len(continent)
    return jsonify({ 'data': { 'countries': countries, 'continents': continent, 'total': total }})

if __name__ == '__main__':
    app.run()