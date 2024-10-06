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

    pitcher_stats = players.get_pitcher_stats() 

    hitter_stats = players.get_hitting_stats()

    non_pitcher_number = []
    pitcher_number = []
    for player in player_list:
        
        if player[7] != 'P':
            non_pitcher_number.append(player)

        else:
            pitcher_number.append(player)
            print('Current Pitcher ', player)

    print(pitcher_stats)
    only_hitters = []
    for p in hitter_stats:
        if p[5] != 'P':
            only_hitters.append(p)

    return render_template('index.html', roster=non_pitcher_number, hitters=only_hitters, pitchers=pitcher_stats, number=pitcher_number)
