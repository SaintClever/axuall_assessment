from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
url = 'https://en.wikipedia.org/wiki/'


@app.route('/<string:user_query>.wiki-search.com')
def index(user_query):
    response = requests.get(url + user_query)
    doc = BeautifulSoup(response.text, 'html.parser')
    div = doc.find('div', class_='mw-parser-output')
    li = div.find_all('li')
    

    links = []
    for link in li:
        if user_query.capitalize() in str(link.text):
            element = link.find(href=True)
            try:
                element_href = element['href']
                links.append(url + element_href[element_href.rfind('/') + 1:])
            except TypeError:
                pass

 
    if links != []:
        return jsonify({'links': [links]})
    else:
        return jsonify({'links': [url + user_query]})
    

if __name__ == '__main__':
    app.run(debug=True)