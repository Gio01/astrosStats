'''
Simple start to see how the API works and also how i can then use that data and push it into 
a simple website to get some Astros stats!
'''

from dataclasses import dataclass
import sqlite3

@dataclass
class Player:
    id: int #primary key
    playerId: int #players id to find them using the mlb api
    fullName: str
    firstName: str
    lastName: str
    primaryNumber: str
    currentTeam: str
    primaryPosition: str
    useName: str
    boxscoreName: str
    nickName: str
    mlbDebutDate: str
    nameFirstLast: str
    nameSlug: str
    firstLastName: str
    lastFirstName: str
    lastInitName: str
    initLastName: str
    fullFMLName: str
    fullLFMName: str


import statsapi


def get_astros_players():
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

    return full_player_desc



def create_player_table():
    sql_statement = [
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                playerId TEXT NOT NULL,
                fullName TEXT NOT NULL,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                primaryNumber TEXT NOT NULL,
                currentTeam TEXT NOT NULL,
                primaryPosition TEXT NOT NULL,
                useName TEXT NOT NULL,
                boxscoreName TEXT NOT NULL,
                nickName TEXT,
                mlbDebutDate TEXT NOT NULL,
                nameSlug TEXT
                );
            """
            ]
    
    try: 
        with sqlite3.connect('mlb.db') as conn:
            cursor = conn.cursor()

            for statement in sql_statement:
                cursor.execute(statement)

            conn.commit()

    except sqlite3.Error as e:
        print(e)

# create a player stat table with all of their data per player based on the playerID used! ensure that the playerID is the 
# primary key used within that other table!

def add_player(conn, player):
    stmt = f'''INSERT INTO players(playerId, fullName, firstName, lastName, primaryNumber, 
        currentTeam, primaryPosition, useName, boxscoreName, nickName, mlbDebutDate, nameSlug)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

    cur = conn.cursor()
    cur.execute(stmt, player)
    conn.commit()
    return cur.lastrowid



def add_data_to_table(player_info):

    players = []
        
    for player in player_info:
        print(player[0])

        players.append((player[0]['id'], player[0]['fullName'], player[0]['firstName'], player[0]['lastName'], 
                        player[0]['primaryNumber'], player[0]['currentTeam']['id'], player[0]['primaryPosition']['abbreviation'], 
                        player[0]['useName'], player[0]['boxscoreName'], player[0].get('nickName'), player[0]['mlbDebutDate'],
                        player[0]['nameSlug']))

    try: 
        with sqlite3.connect('mlb.db') as conn:

            for player in players:

                player_db_id = add_player(conn, player) 

                print('Created the player with the id: ', player_db_id)
    except sqlite3.Error as e:
        print(e)

        


if __name__ == '__main__':
    # create_player_table()
    # player_info = get_astros_players()
    # add_data_to_table(player_info)
    pass
