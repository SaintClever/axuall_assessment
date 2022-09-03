from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_restful import Resource, Api
import requests


app = Flask(__name__)
api = Api(app)
url = 'https://en.wikipedia.org/wiki/'
# @app.route('/<string:user_query>.wiki-search.com')

class Wiki(Resource):
    def get(self, user_query):
        response = requests.get(url + user_query)
        doc = BeautifulSoup(response.text, 'html.parser')
        div = doc.find('div', class_='mw-parser-output')
        li = div.find_all('li')

        # loop through list
        links = []
        for link in li:
            if user_query.capitalize() in str(link.text):
                element = link.find(href=True)
                try:
                    element_href = element['href']
                    links.append(url + element_href[element_href.rfind('/') + 1:])
                except TypeError:
                    pass

        # decide whether to return links or a link
        if links != []:
            return jsonify({'links': [links]})
        else:
            return jsonify({'links': [url + user_query]})
    

api.add_resource(Wiki, '/<string:user_query>.wiki-search.com')


if __name__ == '__main__':
    app.run(debug=True)