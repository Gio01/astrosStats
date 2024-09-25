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
    print(f'Current roster size: {get_roster}')
    array = get_roster.split('\n')
    #print(array)
    
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

    full_player_desc = [] 
    for player in player_obj:

        player_lookup = statsapi.lookup_player(f"{player['firstName']} {player['lastName']}")

        full_player_desc.append(player_lookup)

    print(full_player_desc[0][0])

    print(f'Current stats for {full_player_desc[0][0]["fullName"]} -> {statsapi.player_stat_data(full_player_desc[0][0]["id"])}') 
    print(full_player_desc[0][0].keys())


    return render_template('index.html', team=get_data, roster=player_obj)
#return 'Hello from Astros!'



if __name__ == '__main__':
    app.run(debug=True)
    #print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2008,'gameType':'W'})['people'] if x['fullName']=='Chase Utley'), 'hitting', 'career') )

