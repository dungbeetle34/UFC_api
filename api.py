from flask import render_template, request, jsonify, Flask
from web_scraper import scrape
import sqlite3
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


URL = 'https://www.itnwwe.com/mma/ufc-fighters-roster/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

headers = [th.getText().lower() for th in soup.find_all('thead')[0].find_all('th')]
headers[-1] = 'record'
rows = soup.find_all('tr')[1:]
fighter_info = []

# for i in range(len(rows)):
#     fighter = []
#     for td in rows[i].find_all('td'):
#         fighter.append(td.getText())
#     fighter_info.append(fighter)
fighter_info = [[td.getText() for td in rows[i].find_all('td')] for i in range(len(rows))]

fighterDb = pd.DataFrame(fighter_info[1:], columns=headers)
# json = fighterDb.to_json()
# print(fighterDb.count())

engine = create_engine('sqlite:///fighters.db', echo=True)
sqlite_connection = engine.connect()
sqlite_table = 'Fighters'
fighterDb.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()

app = Flask(__name__)
app.config['DEBUG'] = True

def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/resources/fighters/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('fighters.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_fighters = cur.execute('SELECT * from Fighters;').fetchall()

    return jsonify(all_fighters)

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1><p>Page Not Found</p>', 404

@app.route('/api/v1/resources/fighters', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('index')
    name = query_parameters.get('name')

    query = "SELECT * FROM Fighters WHERE"
    to_filter=[]

    if id:
        query+=' id=? AND'
        to_filter.append(id)
    if name:
        query+=' name=? AND'
        to_filter.append(name)
    if not(id or name):
        return page_not_found(404)
    
    query = query[:-4] + ';'

    conn = sqlite3.connect('fighters.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()






# source ./env/bin/activate (activate environment)
# pip freeze > requirements.txt (to create requirements.txt file)
# pip install -r requirements.txt (to update file with current installations)
# deactivate (leave environment)