from logging import debug
from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import statsapi

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

'''
@app.route('/<team_name>', methods = ['GET'])
def get_team(team_name = None):
    # we can pass the team name to the html page with the param team
    # the left team is the team in the html and team_name is the var set
    # by the user in the html ?
    return render_template('index.html', team=team_name)
#return 'Hello from Astros!'
'''

@app.route('/', methods=['GET'])
def get_astros():
    # we can pass the team name to the html page with the param team
    # the left team is the team in the html and team_name is the var set
    # by the user in the html ?
    astrosId = 117

    get_data = statsapi.get('team', {
        'teamId': astrosId
        })

    get_roster = statsapi.roster(astrosId)
    array = get_roster.split('\n')
    print(array)
    
    player_obj = []

    for player in array:
    
        clean = player.split()
        if len(clean) != 0:

            print(clean)

            player_obj.append({
                'number': clean[0],
                'position': clean[1],
                'firstName': clean[2],
                'lastName': clean[3]
            })

            
    
    print(player_obj)
    return render_template('index.html', team=get_data, roster=player_obj)
#return 'Hello from Astros!'



if __name__ == '__main__':
    app.run(debug=True)
