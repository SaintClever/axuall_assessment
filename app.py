from flask import Flask, jsonify
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
api = Api(app)
url = 'https://en.wikipedia.org/wiki/'
# @app.route('/<string:user_query>.wiki-search.com')


class Wiki(Resource):
    def get(self, user_query) -> jsonify:
        '''CREATE REQUEST'''
        response = requests.get(url + user_query)
        doc = BeautifulSoup(response.text, 'html.parser')

        '''LOCATE DIV AND CHILD LIST'''
        div = doc.find('div', class_='mw-parser-output')
        li = div.find_all('li')

        '''LOOP THROUGH LIST'''
        # links = []
        # for link in li:
        #     if user_query.capitalize() in str(link.text) and\
        #             (element := link.find(href=True)):
        #             element_href = element['href']
        #             # REMOVE /wiki/ from https://en.wikipedia.org/wiki/
        #             links.append(url + element_href[element_href.rfind('/') + 1:])

        '''REFACTOR FOR LOOP'''
        links = [
            url + element['href'][element['href'].rfind('/') + 1:]
            for link in li if user_query.capitalize() in str(link.text) and
            (element := link.find(href=True))
        ]

        '''MAKE SURE HREF LINKS RETURN FIRST ELSE RETURN SINGLE HREF'''
        if links != []:
            return jsonify({'links': links})
        span = doc.find('span', class_='mw-page-title-main').text.replace(' ', '_')
        return jsonify({'links': [url + span]})

# RESOURCE API's
api.add_resource(Wiki, '/<string:user_query>.wiki-search.com')
print(Wiki.get.__annotations__)

if __name__ == '__main__':
    app.run(debug=True)