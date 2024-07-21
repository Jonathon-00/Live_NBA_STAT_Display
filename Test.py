from bs4 import BeautifulSoup 
import requests

def city_to_abbreviation(team_city):
    abbreviations =     {
        'Atlanta': 'ATL',
        'Boston': 'BOS',
        'Brooklyn': 'BRK',
        'Charlotte': 'CHO',
        'Chicago': 'CHI',
        'Cleveland': 'CLE',
        'Dallas': 'DAL',
        'Denver': 'DEN',
        'Detroit': 'DET',
        'Golden State': 'GSW',
        'Houston': 'HOU',
        'Indiana': 'IND',
        'LA Clippers': 'LAC',
        'LA Lakers': 'LAL',
        'Memphis': 'MEM',
        'Miami': 'MIA',
        'Milwaukee': 'MIL',
        'Minnesota': 'MIN',
        'New Orleans': 'NOP',
        'New York': 'NYK',
        'Oklahoma City': 'OKC',
        'Orlando': 'ORL',
        'Philadelphia': 'PHI',
        'Phoenix': 'PHO',
        'Portland': 'POR',
        'Sacramento': 'SAC',
        'San Antonio': 'SAS',
        'Toronto': 'TOR',
        'Utah': 'UTA',
        'Washington': 'WAS'
    }

    return abbreviations.get(team_city, 'Team not found')

def summarize_game_info(games):
    
    game_info = []
    
    for game in games:
    
        winner_location = game.find('tr', class_='winner')
        loser_location = game.find('tr', class_='loser')
        
        winner = winner_location.find('a').get_text()
        loser = loser_location.find('a').get_text()
        winner_score = winner_location.find('td', class_='right').get_text()
        loser_score = loser_location.find('td', class_='right').get_text()
        OT = winner_location.find_all('td', class_='right')
        close_game = False
        if int(winner_score) <= int(loser_score) + 5 or OT[1].get_text(strip=True) == 'OT':
            close_game = True

        


        game_links = game.find('p', class_='links')
        boxscore_link = game_links.find('a').get('href')
        boxscore_url = website + boxscore_link

        boxscore_result = requests.get(boxscore_url)
        boxscore_site_content= boxscore_result.text
        boxscore_soup = BeautifulSoup(boxscore_site_content, 'html.parser')
        boxscores = boxscore_soup.find('div', id='content')

        winner_abrv = city_to_abbreviation(winner)
        winner_boxscore = boxscores.find('div', id='all_box-' + winner_abrv + '-game-basic')
        winner_team_stats = winner_boxscore.find('tfoot')
        winner_statline = winner_team_stats.find_all('td', class_='right')
        winner_FG = winner_statline[1].get_text()
        winner_FGA = winner_statline[2].get_text()
        winner_FGpercent = winner_statline[3].get_text()
        winner_3P = winner_statline[4].get_text()
        winner_3PA = winner_statline[5].get_text()
        winner_3Ppercent = winner_statline[6].get_text()
        winner_FT = winner_statline[7].get_text()
        winner_FTA = winner_statline[8].get_text()
        winner_FTpercent = winner_statline[9].get_text()
        winner_ORB = winner_statline[10].get_text()
        winner_TRB = winner_statline[12].get_text()
        winner_TOV = winner_statline[16].get_text()

        loser_abrv = city_to_abbreviation(loser)
        loser_boxscore = boxscores.find('div', id='all_box-' + loser_abrv + '-game-basic')
        loser_team_stats = loser_boxscore.find('tfoot')
        loser_statline = loser_team_stats.find_all('td', class_='right')
        loser_FG = loser_statline[1].get_text()
        loser_FGA = loser_statline[2].get_text()
        loser_FGpercent = loser_statline[3].get_text()
        loser_3P = loser_statline[4].get_text()
        loser_3PA = loser_statline[5].get_text()
        loser_3Ppercent = loser_statline[6].get_text()
        loser_FT = loser_statline[7].get_text()
        loser_FTA = loser_statline[8].get_text()
        loser_FTpercent = loser_statline[9].get_text()
        loser_ORB = loser_statline[10].get_text()
        loser_TRB = loser_statline[12].get_text()
        loser_TOV = loser_statline[16].get_text()


        winner_player_stats_location = winner_boxscore.find('tbody')
        winner_player_statlines = winner_player_stats_location.find_all('tr')
        del winner_player_statlines[5]
        
        winner_PTS_leader = 0
        winner_TRB_leader = 0
        winner_AST_leader = 0
        winner_STL_leader = 0
        winner_BLK_leader = 0
        winner_PTS_leader_mp = 0
        winner_AST_leader_mp = 0
        winner_TRB_leader_mp = 0
        winner_STL_leader_mp = 0
        winner_BLK_leader_mp = 0 

        for player in winner_player_statlines:
            player_name = player.find('a').get_text()
            player_name = player_name.encode('iso-8859-1').decode('utf-8')
            player_stats = player.find_all('td', class_='right')
            if len(player_stats) > 10:
                player_TRB = player_stats[12].get_text()
                player_AST = player_stats[13].get_text()
                player_STL = player_stats[14].get_text()
                player_BLK = player_stats[15].get_text()
                player_PTS = player_stats[18].get_text()
                player_MP = player_stats[0].get_text()
                player_MP = str(float(player_MP.split(':')[0]) + float(player_MP.split(':')[1])/60)

            if (int(player_TRB) > int(winner_TRB_leader)) or ((int(player_TRB) == int(winner_TRB_leader)) and (float(player_MP) < float(winner_TRB_leader_mp))):
                winner_TRB_leader = player_TRB
                winner_TRB_leader_name = player_name
                winner_TRB_leader_mp = player_MP
            if (int(player_AST) > int(winner_AST_leader)) or ((int(player_AST) == int(winner_AST_leader)) and (float(player_MP) < float(winner_AST_leader_mp))):
                winner_AST_leader = player_AST
                winner_AST_leader_name = player_name
                winner_AST_leader_mp = player_MP
            if (int(player_STL) > int(winner_STL_leader)) or ((int(player_STL) == int(winner_STL_leader)) and (float(player_MP) < float(winner_STL_leader_mp))):
                winner_STL_leader = player_STL
                winner_STL_leader_name = player_name
                winner_STL_leader_mp = player_MP
            if (int(player_BLK) > int(winner_BLK_leader)) or ((int(player_BLK) == int(winner_BLK_leader)) and (float(player_MP) < float(winner_BLK_leader_mp))):
                winner_BLK_leader = player_BLK
                winner_BLK_leader_name = player_name
                winner_BLK_leader_mp = player_MP
            if (int(player_PTS) > int(winner_PTS_leader)) or ((int(player_PTS) == int(winner_PTS_leader)) and (float(player_MP) < float(winner_PTS_leader_mp))):
                winner_PTS_leader = player_PTS
                winner_PTS_leader_name = player_name
                winner_PTS_leader_mp = player_MP

        loser_player_stats_location = loser_boxscore.find('tbody')
        loser_player_statlines = loser_player_stats_location.find_all('tr')
        del loser_player_statlines[5]
        
        loser_PTS_leader = 0
        loser_TRB_leader = 0
        loser_AST_leader = 0
        loser_STL_leader = 0
        loser_BLK_leader = 0
        loser_PTS_leader_mp = 0
        loser_AST_leader_mp = 0
        loser_TRB_leader_mp = 0
        loser_STL_leader_mp = 0
        loser_BLK_leader_mp = 0


        for player in loser_player_statlines:
            player_name = player.find('a').get_text()
            player_name = player_name.encode('iso-8859-1').decode('utf-8')
            player_stats = player.find_all('td', class_='right')
            if len(player_stats) > 10:
                player_TRB = player_stats[12].get_text()
                player_AST = player_stats[13].get_text()
                player_STL = player_stats[14].get_text()
                player_BLK = player_stats[15].get_text()
                player_PTS = player_stats[18].get_text()
                player_MP = player_stats[0].get_text()
                player_MP = str(float(player_MP.split(':')[0]) + float(player_MP.split(':')[1])/60)
            
            if (int(player_TRB) > int(loser_TRB_leader)) or ((int(player_TRB) == int(loser_TRB_leader)) and (float(player_MP) < float(loser_TRB_leader_mp))):
                loser_TRB_leader = player_TRB
                loser_TRB_leader_name = player_name
                loser_TRB_leader_mp = player_MP
            if (int(player_AST) > int(loser_AST_leader)) or ((int(player_AST) == int(loser_AST_leader)) and (float(player_MP) < float(loser_AST_leader_mp))):
                loser_AST_leader = player_AST
                loser_AST_leader_name = player_name
                loser_AST_leader_mp = player_MP
            if (int(player_STL) > int(loser_STL_leader)) or ((int(player_STL) == int(loser_STL_leader)) and (float(player_MP) < float(loser_STL_leader_mp))):
                loser_STL_leader = player_STL
                loser_STL_leader_name = player_name
                loser_STL_leader_mp = player_MP
            if (int(player_BLK) > int(loser_BLK_leader)) or ((int(player_BLK) == int(loser_BLK_leader)) and (float(player_MP) < float(loser_BLK_leader_mp))):
                loser_BLK_leader = player_BLK
                loser_BLK_leader_name = player_name
                loser_BLK_leader_mp = player_MP
            if (int(player_PTS) > int(loser_PTS_leader)) or ((int(player_PTS) == int(loser_PTS_leader)) and (float(player_MP) < float(loser_PTS_leader_mp))):
                loser_PTS_leader = player_PTS
                loser_PTS_leader_name = player_name
                loser_PTS_leader_mp = player_MP


        thisdict = { "winner": {"team": winner, "score": winner_score, 
                                "team_stats": {"FG": winner_FG, "FGA": winner_FGA, "FG%": winner_FGpercent, 
                                        "3P": winner_3P, "3PA": winner_3PA, "3P%": winner_3Ppercent, 
                                        "FT": winner_FT, "FTA": winner_FTA, "FT%": winner_FTpercent, 
                                        "ORB": winner_ORB, "TRB": winner_TRB, "TOV": winner_TOV},
                                "player_stats": {"PTS_leader": [winner_PTS_leader, winner_PTS_leader_name], 
                                                "TRB_leader": [winner_TRB_leader, winner_TRB_leader_name], 
                                                "AST_leader": [winner_AST_leader, winner_AST_leader_name], 
                                                "STL_leader": [winner_STL_leader, winner_STL_leader_name], 
                                                "BLK_leader": [winner_BLK_leader, winner_BLK_leader_name]}},
        
                    "loser": {"team": loser, "score": loser_score,
                            "team_stats": {"FG": loser_FG, "FGA": loser_FGA, "FG%": loser_FGpercent, 
                                        "3P": loser_3P, "3PA": loser_3PA, "3P%": loser_3Ppercent, 
                                        "FT": loser_FT, "FTA": loser_FTA, "FT%": loser_FTpercent, 
                                        "ORB": loser_ORB, "TRB": loser_TRB, "TOV": loser_TOV},
                                "player_stats": {"PTS_leader": [loser_PTS_leader, loser_PTS_leader_name], 
                                                "TRB_leader": [loser_TRB_leader, loser_TRB_leader_name], 
                                                "AST_leader": [loser_AST_leader, loser_AST_leader_name], 
                                                "STL_leader": [loser_STL_leader, loser_STL_leader_name], 
                                                "BLK_leader": [loser_BLK_leader, loser_BLK_leader_name]}},
                    "close_game": close_game}

        game_info.append(thisdict)

    return game_info

def get_offensive_and_defensive_ratings():
    ratings_url = website + '/leagues/NBA_2024_ratings.html'

    ratings_result = requests.get(ratings_url)
    ratings_site_content = ratings_result.text
    ratings_soup = BeautifulSoup(ratings_site_content, 'html.parser')

    ratings_location = ratings_soup.find('div', id='div_ratings')
    ratings_table = ratings_location.find('tbody')
    team_ratings = ratings_table.find_all('tr')

    thisdict = {}

    for team in team_ratings:
        team_name = team.find('a').get_text()
        team_ratings = team.find_all('td', class_='right')
        team_offensive_rating = team_ratings[4].get_text()
        team_defensive_rating = team_ratings[5].get_text()

        thisdict[team_name] = [team_offensive_rating, 0, team_defensive_rating, 0]


    Rtg_list = list(thisdict.values())
    team_list = list(thisdict.keys())
    ORtg_list = [float(i[0]) for i in Rtg_list]
    DRtg_list = [float(i[2]) for i in Rtg_list]

    ORtg_list_sorted = sorted(ORtg_list)
    DRtg_list_sorted = sorted(DRtg_list)

    for i in range(len(ORtg_list)):
        ORtg = ORtg_list_sorted[i]
        DRtg = DRtg_list_sorted[i]

        ORtg_index = ORtg_list.index(ORtg)
        DRtg_index = DRtg_list.index(DRtg)

        ORtg_team_name = team_list[ORtg_index]
        DRtg_team_name = team_list[DRtg_index]

        thisdict[ORtg_team_name][1] = 30-i
        thisdict[DRtg_team_name][3] = i+1

    return thisdict

def summarize_standings(standings):
    east_standings = standings.find('table', id='confs_standings_E')
    west_standings = standings.find('table', id='confs_standings_W')

    offensive_and_defensive_ratings = get_offensive_and_defensive_ratings()

    east_team_standings = []
    west_team_standings = []

    east_standings_teams = east_standings.find_all('tr', class_='full_table')
    west_standings_teams = west_standings.find_all('tr', class_='full_table')

    for team in east_standings_teams:
        team_name = team.find('a').get_text()
        team_record = team.find_all('td', class_='right')
        team_wins = team_record[0].get_text()
        team_losses = team_record[1].get_text()
        team_WL_pct = team_record[2].get_text()

        team_ORtg = offensive_and_defensive_ratings[team_name][0]
        team_DRtg = offensive_and_defensive_ratings[team_name][1]

        thisdict = {"team": team_name, "wins": team_wins, "losses": team_losses, "WL_pct": team_WL_pct, "ORtg": team_ORtg, "DRtg": team_DRtg}

        east_team_standings.append(thisdict)

    for team in west_standings_teams:
        team_name = team.find('a').get_text()
        team_record = team.find_all('td', class_='right')
        team_wins = team_record[0].get_text()
        team_losses = team_record[1].get_text()
        team_WL_pct = team_record[2].get_text()

        team_ORtg = offensive_and_defensive_ratings[team_name][0]
        team_ORtg_rank = offensive_and_defensive_ratings[team_name][1]
        team_DRtg = offensive_and_defensive_ratings[team_name][2]
        team_DRtg_rank = offensive_and_defensive_ratings[team_name][3]

        thisdict = {"team": team_name, "wins": team_wins, "losses": team_losses, "WL_pct": team_WL_pct, "ORtg": team_ORtg, "ORtg_rank":team_ORtg_rank, "DRtg": team_DRtg, "DRtg_rank": team_DRtg_rank}

        west_team_standings.append(thisdict)
    
    return [east_team_standings, west_team_standings]

def get_top_twenty_leaders(leaders_location):
    leaders_table = leaders_location.find('table', class_='columns')
    leaders_rows = leaders_table.find_all('tr')
    
    leaders = []

    for row in leaders_rows:
        name_loaction = row.find('td', class_='who')
        
        name = name_loaction.find('a').get_text()
        value = row.find('td', class_='value').get_text()
        name = name.encode('iso-8859-1').decode('utf-8')

        leaders.append([name, value])
    
    return leaders


def get_stat_leaders():
    stat_leaders_url = website + '/leagues/NBA_2024_leaders.html'
    stat_leaders_result = requests.get(stat_leaders_url)
    stat_leaders_site_content = stat_leaders_result.text
    stat_leaders_soup = BeautifulSoup(stat_leaders_site_content, 'html.parser')
    stat_location = stat_leaders_soup.find('div', id='content')
    stat_leaders_location= stat_location.find('div', class_='data_grid')


    ppg_leaders_location = stat_leaders_location.find('div', id='leaders_pts_per_g')
    rpg_leaders_location = stat_leaders_location.find('div', id='leaders_trb_per_g')
    apg_leaders_location = stat_leaders_location.find('div', id='leaders_ast_per_g')
    spg_leaders_location = stat_leaders_location.find('div', id='leaders_stl_per_g')
    bpg_leaders_location = stat_leaders_location.find('div', id='leaders_blk_per_g')
    fg3_pct_leaders_location = stat_leaders_location.find('div', id='leaders_fg3_pct')
    bpm_leaders_location = stat_leaders_location.find('div', id='leaders_bpm')

    ppg_leaders = get_top_twenty_leaders(ppg_leaders_location)
    rpg_leaders = get_top_twenty_leaders(rpg_leaders_location)
    apg_leaders = get_top_twenty_leaders(apg_leaders_location)
    spg_leaders = get_top_twenty_leaders(spg_leaders_location)
    bpg_leaders = get_top_twenty_leaders(bpg_leaders_location)
    fg3_pct_leaders = get_top_twenty_leaders(fg3_pct_leaders_location)
    bpm_leaders = get_top_twenty_leaders(bpm_leaders_location)

    return {"PPG": ppg_leaders, "RPG": rpg_leaders, "APG": apg_leaders, "SPG": spg_leaders, "BPG": bpg_leaders, "FG3%": fg3_pct_leaders, "BPM": bpm_leaders}





website = 'https://www.basketball-reference.com'

recent_games_website = website + '/boxscores/'
recent_games_result = requests.get(recent_games_website)
recent_games_site_content= recent_games_result.text
recent_games_soup = BeautifulSoup(recent_games_site_content, 'html.parser')

recent_games = recent_games_soup.find('div', id='content')
game_summaries = recent_games.find('div', class_='game_summaries')
standings = recent_games.find('div', class_='standings_confs data_grid section_wrapper')
games = game_summaries.find_all('div', class_='game_summary expanded nohover')

game_info = summarize_game_info(games)
print(game_info)

standing_info = summarize_standings(standings)
east_standings = standing_info[0]
west_standings = standing_info[1]
print(east_standings)
print(west_standings)


stat_leaders_info = get_stat_leaders()
print(stat_leaders_info)



    
    
    
    
    
