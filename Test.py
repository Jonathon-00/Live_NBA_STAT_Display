from bs4 import BeautifulSoup 
import requests

def city_to_abbreviation(team_city):
    abbreviations =     {
        'Atlanta': 'ATL',
        'Boston': 'BOS',
        'Brooklyn': 'BKN',
        'Charlotte': 'CHA',
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


website = 'https://www.basketball-reference.com'

recent_games_website = website + '/boxscores/'
recent_games_result = requests.get(recent_games_website)
recent_games_site_content= recent_games_result.text
recent_games_soup = BeautifulSoup(recent_games_site_content, 'html.parser')

recent_games = recent_games_soup.find('div', id='content')
game_summaries = recent_games.find('div', class_='game_summaries')
standings = recent_games.find('div', class_='standings_confs data_grid section_wrapper')
east_standings = standings.find('table', id='confs_standings_E')
west_standings = standings.find('table', id='confs_standings_W')

games = game_summaries.find_all('div', class_='game_summary expanded nohover')

print('Number of games:', len(games))

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





    thisdict = { "winner": {"team": winner, "score": winner_score, 
                            "team_stats": {"FG": winner_FG, "FGA": winner_FGA, "FG%": winner_FGpercent, 
                                      "3P": winner_3P, "3PA": winner_3PA, "3P%": winner_3Ppercent, 
                                      "FT": winner_FT, "FTA": winner_FTA, "FT%": winner_FTpercent, 
                                      "ORB": winner_ORB, "TRB": winner_TRB, "TOV": winner_TOV}},
                "loser": {"team": loser, "score": loser_score,
                          "team_stats": {"FG": loser_FG, "FGA": loser_FGA, "FG%": loser_FGpercent, 
                                    "3P": loser_3P, "3PA": loser_3PA, "3P%": loser_3Ppercent, 
                                     "FT": loser_FT, "FTA": loser_FTA, "FT%": loser_FTpercent, 
                                     "ORB": loser_ORB, "TRB": loser_TRB, "TOV": loser_TOV}},
                "close_game": close_game}

    game_info.append(thisdict)


print(game_info)





def city_to_abbreviation(team_city):
    abbreviations =     {
        'Atlanta': 'ATL',
        'Boston': 'BOS',
        'Brooklyn': 'BKN',
        'Charlotte': 'CHA',
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



    
    
    
    
    
