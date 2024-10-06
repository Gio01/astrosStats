'''
Simple start to see how the API works and also how i can then use that data and push it into 
a simple website to get some Astros stats!
'''
import sqlite3
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

        

###############
# Create a table with the Hitting stats!
###############
from dao import DAO


def get_astros_hitting_stats():

    players = DAO()

    player_list = players.get_db_data()
    hitter_stat = []
    for player in player_list:

        player_stat = statsapi.player_stat_data(player[1], group="[hitting]", type="season")
        # for the most part this if will remove pitchers since they tend to not bat at all
        if len(player_stat.get('stats')) != 0:
            print('Player info for: ', player_stat.get('first_name'), '\n')
            print(player_stat, '\n')
            #print(player_stat.get('stats')[0].get('stats'))

            hitter_stat.append(player_stat)

    return hitter_stat


def create_hitter_stat_table():
    sql_statement = [
        """
        CREATE TABLE IF NOT EXISTS hitting_stats(
        id INTEGER PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL, 
        active TEXT NOT NULL,
        currentTeam TEXT NOT NULL,
        position TEXT NOT NULL,
        season TEXT NOT NULL,
        gamesPlayed INTEGER NOT NULL,
        groundOuts INTEGER NOT NULL,
        airOuts INTEGER NOT NULL,
        runs INTEGER NOT NULL,
        doubles INTEGER NOT NULL,
        triples INTEGER NOT NULL,
        homeRuns INTEGER NOT NULL,
        strikeOuts INTEGER NOT NULL,
        baseOnBalls INTEGER NOT NULL,
        intentionalWalks INTEGER NOT NULL,
        hits INTEGER NOT NULL,
        hitByPitch INTEGER,
        avg TEXT NOT NULL,
        atBats INTEGER NOT NULL,
        obp TEXT NOT NULL,
        slg TEXT NOT NULL,
        ops TEXT NOT NULL,
        caughtStealing INTEGER NOT NULL,
        stolenBases INTEGER NOT NULL,
        stolenBasePercentage TEXT NOT NULL,
        groundIntoDoublePlay INTEGER NOT NULL,
        numberOfPitches INTEGER NOT NULL,
        plateAppearances INTEGER NOT NULL,
        totalBases INTEGER NOT NULL,
        rbi INTEGER NOT NULL,
        leftOnBase INTEGER NOT NULL,
        sacBunts INTEGER NOT NULL,
        sacFlies INTEGER NOT NULL,
        babip TEXT NOT NULL,
        groundOutsToAirouts TEXT NOT NULL,
        catchersInterference INTEGER NOT NULL,
        atBatsPerHomeRun TEXT NOT NULL 
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


def add_hitting_data_to_table():
    
    hitter_stat = get_astros_hitting_stats()
    hitters = []

    for hitter in hitter_stat:
        getter = hitter.get('stats')[0].get('stats')
        #print('Single Hitter data: ', hitter)

        hitters.append((hitter.get('id'), #0 
            hitter.get('first_name'),
            hitter.get('last_name'),
            hitter.get('active'),
            hitter.get('current_team'),
            hitter.get('position'),
            hitter.get('stats')[0].get('season'),

            getter.get('gamesPlayed'),
            getter.get('groundOuts'),
            getter.get('airOuts'),
            getter.get('runs'),#10
            getter.get('doubles'),
            getter.get('triples'),
            getter.get('homeRuns'),#13
            getter.get('strikeOuts'),#14
            getter.get('baseOnBalls'),#15
            getter.get('intentionalWalks'),
            getter.get('hits'),#17
            getter.get('hitsByPitch'),
            getter.get('avg'),#19
            getter.get('atBats'), #20
            getter.get('obp'),
            getter.get('slg'),
            getter.get('ops'),
            getter.get('caughtStealing'),
            getter.get('stolenBases'),
            getter.get('stolenBasePercentage'),
            getter.get('groundIntoDoublePlay'),
            getter.get('numberOfPitches'),
            getter.get('plateAppearances'),
            getter.get('totalBases'),
            getter.get('rbi'),#31
            getter.get('leftOnBase'),
            getter.get('sacBunts'),
            getter.get('sacFlies'),
            getter.get('babip'),
            getter.get('groundOutsToAirouts'),
            getter.get('catchersInterference'),
            getter.get('atBatsPerHomeRun'),
        ))

    try: 
        with sqlite3.connect('mlb.db') as conn:

            for hitter in hitters:

                hitter_id = add_hitting_stats(conn, hitter) 

                print('Created the hitter with the id: ', hitter_id)
    except sqlite3.Error as e:
        print(e)


def add_hitting_stats(conn, player):
    stmt = f'''INSERT INTO hitting_stats(
        id,
        firstName,
        lastName, 
        active,
        currentTeam,
        position,
        season,
        gamesPlayed,
        groundOuts,
        airOuts,
        runs,
        doubles,
        triples,
        homeRuns,
        strikeOuts,
        baseOnBalls,
        intentionalWalks,
        hits,
        hitByPitch,
        avg,
        atBats,
        obp,
        slg,
        ops,
        caughtStealing,
        stolenBases,
        stolenBasePercentage,
        groundIntoDoublePlay,
        numberOfPitches,
        plateAppearances,
        totalBases,
        rbi,
        leftOnBase,
        sacBunts,
        sacFlies,
        babip,
        groundOutsToAirouts,
        catchersInterference,
        atBatsPerHomeRun 
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?)
        '''

    cur = conn.cursor()
    cur.execute(stmt, player)
    conn.commit()
    return cur.lastrowid


###############
# Create a table with the Pitcher stats!
###############
def get_pitcher_stats():

    players_list = DAO()

    players = players_list.get_db_data()

    pitchers = []

    pitcher_stats = []
    for player in players:
        if player[7] == 'P':
            pitchers.append(player)
    
    for pitcher in pitchers:
        pitcher_stat = statsapi.player_stat_data(pitcher[1], group="[pitching]", type="season")
        print('Player Info for: ', pitcher_stat.get('first_name'), '\n')

        print(pitcher_stat)
        #print(pitcher_stat.get('stats'))

        #print('Actual stats: ', pitcher_stat.get('stats')[0].get('stats'))

        pitcher_stats.append(pitcher_stat)
    
    return pitcher_stats


def create_pitcher_stat_table():
    sql_statement = [
        """
        CREATE TABLE IF NOT EXISTS pitcher_stats(
        id INTEGER PRIMARY KEY,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL, 
        active TEXT NOT NULL,
        currentTeam TEXT NOT NULL,
        position TEXT NOT NULL,
        season TEXT NOT NULL,
        gamesPlayed INTEGER NOT NULL,
        gamesStarted INTEGER NOT NULL,
        groundOuts INETEGER NOT NULL,
        airOuts INTEGER NOT NULL,
        runs INTEGER NOT NULL,
        doubles INTEGER NOT NULL,
        triples INTEGER NOT NULL,
        homeRuns INTEGER NOT NULL,
        strikeOuts INTEGER NOT NULL,
        baseOnBalls INTEGER NOT NULL,
        intentionalWalks INTEGER NOT NULL,
        hits INTEGER NOT NULL,
        hitByPitch INTEGER NOT NULL,
        avg TEXT NOT NULL, 
        atBats TEXT NOT NULL,
        obp TEXT NOT NULL,
        slg TEXT NOT NULL, 
        ops TEXT NOT NULL,
        caughtStealing INTEGER NOT NULL,
        stolenBases INTEGER NO NULL,
        stolenBasePercentage TEXT NOT NULL,
        groundIntoDoublePlay INTEGER NOT NULL,
        numberOfPitches INTEGER NOT NULL,
        era TEXT NOT NULL,
        inningsPitched TEXT NOT NULL,
        wins INTEGER NOT NULL,
        losses INTEGER NOT NULL,
        saves INTEGER NOT NULL,
        saveOpportunities INTEGER NOT NULL,
        holds INTEGER NOT NULL,
        blownSaves INTEGER NOT NULL,
        earnedRuns INTEGER NOT NULL,
        whip TEXT NOT NULL,
        battersFaced INTEGER NOT NULL,
        outs INTEGER NOT NULL,
        gamesPitched INTEGER NOT NULL,
        completeGames INTEGER NOT NULL,
        shutouts INTEGER NOT NULL,
        strikes INTEGER NOT NULL,
        strikePercentage TEXT NOT NULL,
        hitBatsmen INTEGER NOT NULL,
        balks INTEGER NOT NULL,
        wildPitches INTEGER NOT NULL,
        pickoffs INTEGER NOT NULL,
        totalBases INTEGER NOT NULL,
        groundOutsToAirouts TEXT NOT NULL,
        winPercentage TEXT NOT NULL,
        pitchesPerInning TEXT NOT NULL,
        gamesFinished INTEGER NOT NULL,
        strikeoutWalkRatio TEXT NOT NULL,
        strikeoutsPer9Inn TEXT NOT NULL,
        walksPer9Inn TEXT NOT NULL,
        hitsPer9Inn TEXT NOT NULL,
        runsScoredPer9 TEXT NOT NULL,
        homeRunsPer9 TEXT NOT NULL,
        inheritedRunners INTEGER NOT NULL,
        inheritedRunnersScored INTEGER NOT NULL,
        catchersInterferance INTEGER,
        sacBunts INTEGER NOT NULL,
        sacFlies INTEGER NOT NULL 
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



def create_player_stat_table():
    sql_statement = [
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                playerId TEXT NOT NULL,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                active BOOL NOT NULL,
                current_team TEXT NOT NULL,
                position TEXT NOT NULL,
                nickName TEXT,
                lastPlayed TEXT,
                mlbDebut TEXT NOT NULL,
                bat_side TEXT NOT NULL, 
                pitchHand TEXT NOT NULL,
                ;
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


def add_pitcher_data_to_table():
    
    pitcher_stats = get_pitcher_stats()
    pitchers = []
    for player in pitcher_stats:
        print('Single Pitcher data: ',player)
        
        pitchers.append((player['id'], #0  
                        player['first_name'], player['last_name'], player['active'], #1, 2, 3
                        player['current_team'], player['position'], player.get('stats')[0].get('season'), # 4, 5, 6
                        player.get('stats')[0].get('stats').get('gamesPlayed'), player.get('stats')[0].get('stats').get('gamesStarted'), #7 8 
                        player.get('stats')[0].get('stats').get('groundOuts'), player.get('stats')[0].get('stats').get('airOuts'), #9 10
                        player.get('stats')[0].get('stats').get('runs'), player.get('stats')[0].get('stats').get('doubles'), #11 12
                        player.get('stats')[0].get('stats').get('triples'), player.get('stats')[0].get('stats').get('homeRuns'), #13 14
            
                        player.get('stats')[0].get('stats').get('strikeOuts'), player.get('stats')[0].get('stats').get('baseOnBalls'), #15 16 
                        player.get('stats')[0].get('stats').get('intentionalWalks'), player.get('stats')[0].get('stats').get('hits'), #17 18 
                        player.get('stats')[0].get('stats').get('hitByPitch'), player.get('stats')[0].get('stats').get('avg'), #19 20
                        player.get('stats')[0].get('stats').get('atBats'), player.get('stats')[0].get('stats').get('obp'), # 21 22
                        player.get('stats')[0].get('stats').get('slg'), player.get('stats')[0].get('stats').get('ops'), #23 24
                        player.get('stats')[0].get('stats').get('caughtStealing'), player.get('stats')[0].get('stats').get('stolenBases'), #25 26 
                        
                        player.get('stats')[0].get('stats').get('stolenBasePercentage'), player.get('stats')[0].get('stats').get('groundIntoDoublePlay'), #27 28 
                        
                        player.get('stats')[0].get('stats').get('numberOfPitches'), player.get('stats')[0].get('stats').get('era'), #29 #30
                        player.get('stats')[0].get('stats').get('inningsPitched'), player.get('stats')[0].get('stats').get('wins'), #31 32 
                        player.get('stats')[0].get('stats').get('losses'), player.get('stats')[0].get('stats').get('saves'), #33 34 
                        player.get('stats')[0].get('stats').get('saveOpportunities'), player.get('stats')[0].get('stats').get('holds'), #35 36 
                        player.get('stats')[0].get('stats').get('blownSaves'), player.get('stats')[0].get('stats').get('earnedRuns'), #37 38
                        player.get('stats')[0].get('stats').get('whip'), player.get('stats')[0].get('stats').get('battersFaced'), # 39 40

                        player.get('stats')[0].get('stats').get('outs'), player.get('stats')[0].get('stats').get('gamesPitched'), #41 42
                        player.get('stats')[0].get('stats').get('completeGames'), player.get('stats')[0].get('stats').get('shutouts'), #43 44
                        player.get('stats')[0].get('stats').get('strikes'), player.get('stats')[0].get('stats').get('strikePercentage'), #45 46
                        player.get('stats')[0].get('stats').get('hitBatsmen'), player.get('stats')[0].get('stats').get('balks'), #47 48
                        player.get('stats')[0].get('stats').get('wildPitches'), player.get('stats')[0].get('stats').get('pickoffs'), #49 50 
                        player.get('stats')[0].get('stats').get('totalBases'), player.get('stats')[0].get('stats').get('groundOutsToAirouts'),#51 52 
                        player.get('stats')[0].get('stats').get('winPercentage'), player.get('stats')[0].get('stats').get('pitchesPerInning'),#53 54 

                        player.get('stats')[0].get('stats').get('gamesFinished'), player.get('stats')[0].get('stats').get('strikeoutWalkRatio'), #55 56
                        player.get('stats')[0].get('stats').get('strikeoutsPer9Inn'), player.get('stats')[0].get('stats').get('walksPer9Inn'), #57 58
                        player.get('stats')[0].get('stats').get('hitsPer9Inn'), player.get('stats')[0].get('stats').get('runsScoredPer9'), #59 60 
                        player.get('stats')[0].get('stats').get('homeRunsPer9'), player.get('stats')[0].get('stats').get('inheritedRunners'), #61 62
                        player.get('stats')[0].get('stats').get('inheritedRunnersScored'), player.get('stats')[0].get('stats').get('catchersInterferance'),#63 64 
                        player.get('stats')[0].get('stats').get('sacBunts'), player.get('stats')[0].get('stats').get('sacFlies'), #65 66
                      ))
    
    try: 
        with sqlite3.connect('mlb.db') as conn:

            for pitcher in pitchers:

                pitcher_db_id = add_pitcher_stats(conn, pitcher) 

                print('Created the pitcher with the id: ', pitcher_db_id)
    except sqlite3.Error as e:
        print(e)

def add_pitcher_stats(conn, player):
    stmt = f'''INSERT INTO pitcher_stats(
        id,
        firstName,
        lastName, 
        active,
        currentTeam,
        position,
        season ,
        gamesPlayed,
        gamesStarted,
        groundOuts,
        airOuts,
        runs,
        doubles,
        triples,
        homeRuns,
        strikeOuts,
        baseOnBalls,
        intentionalWalks,
        hits,
        hitByPitch,
        avg, 
        atBats,
        obp,
        slg, 
        ops,
        caughtStealing,
        stolenBases,
        stolenBasePercentage,
        groundIntoDoublePlay,
        numberOfPitches,
        era,
        inningsPitched,
        wins,
        losses,
        saves,
        saveOpportunities,
        holds,
        blownSaves,
        earnedRuns,
        whip,
        battersFaced,
        outs,
        gamesPitched,
        completeGames,
        shutouts,
        strikes,
        strikePercentage,
        hitBatsmen,
        balks,
        wildPitches,
        pickoffs,
        totalBases,
        groundOutsToAirouts,
        winPercentage,
        pitchesPerInning,
        gamesFinished,
        strikeoutWalkRatio,
        strikeoutsPer9Inn,
        walksPer9Inn,
        hitsPer9Inn,
        runsScoredPer9,
        homeRunsPer9,
        inheritedRunners,
        inheritedRunnersScored,
        catchersInterferance,
        sacBunts,
        sacFlies 
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?)
        '''

    cur = conn.cursor()
    cur.execute(stmt, player)
    conn.commit()
    return cur.lastrowid


if __name__ == '__main__':
    #create_player_table()
    #player_info = get_astros_players()
    #add_data_to_table(player_info)
    #print(get_astros_player_stats())
    #create_pitcher_stat_table()
    #print(add_pitcher_data_to_table()) 
    #get_astros_hitting_stats()
    #create_hitter_stat_table()
    #add_hitting_data_to_table()
    get_pitcher_stats()
