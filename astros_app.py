from logging import debug
from types import MethodType
from flask import Flask, render_template
import json
import sqlite3
import statsapi
from server.dao import DAO

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def get_db_data():

    players = DAO()

    player_list = players.get_db_data()
    print(players)
    return render_template('index.html', roster=player_list)

   


