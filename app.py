from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)
url = 'https://en.wikipedia.org/wiki/'
# @app.route('/<string:user_query>.wiki-search.com')


class Wiki(Resource):
    def get(self, user_query) -> 'json':
        '''REATE REQUEST'''
        response = requests.get(url + user_query)
        doc = BeautifulSoup(response.text, 'html.parser')


        '''LOCATE DIV AND CHILD LIST'''
        div = doc.find('div', class_='mw-parser-output')
        li = div.find_all('li')


        '''LOOP THROUGH LIST'''
        links = []
        for link in li:
            if user_query.capitalize() in str(link.text):
                # element = link.find(href=True)
                # if element:
                if element := link.find(href=True):
                    element_href = element['href']
                    links.append(url + element_href[element_href.rfind('/') + 1:]) # REMOVE /wiki/


        '''MAKE SURE HREF LINKS RETURN FIRST ELSE RETURN SINGLE HREF'''
        if links != []:
            return jsonify({'links': [links]})
        else:
            return jsonify({'links': [url + user_query]})


# RESOURCE API's
api.add_resource(Wiki, '/<string:user_query>.wiki-search.com')
print(Wiki.get.__annotations__)

if __name__ == '__main__':
    app.run(debug=True)