from bs4 import BeautifulSoup 
import requests

website = 'https://www.basketball-reference.com'

class get_data:
    def __init__(self):
        self.games = self.get_recent_games()
        print(self.games)

        self.standings = self.get_standings()
        print(self.standings[0])
        print(self.standings[1])

        self.stat_leaders = self.get_stat_leaders()
        print(self.stat_leaders)

    def get_soup(self, url):
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        return soup
    
    def is_close_game(self, winner_score, loser_score, OT):
        if OT[1].get_text(strip=True) == 'OT':
            return True
        elif int(winner_score) <= int(loser_score) + 5:
            return True
        else:
            return False
        
    def city_to_abrv(self, city):
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

        return abbreviations.get(city, 'Team not found')

    def get_team_stats(self, boxscore):
        team_stats = boxscore.find('tfoot')
        statline = team_stats.find_all('td', class_='right')
        FG = statline[1].get_text()
        FGA = statline[2].get_text()
        FGpercent = statline[3].get_text()
        threeP = statline[4].get_text()
        threePA = statline[5].get_text()
        threePpercent = statline[6].get_text()
        FT = statline[7].get_text()
        FTA = statline[8].get_text()
        FTpercent = statline[9].get_text()
        ORB = statline[10].get_text()
        TRB = statline[12].get_text()
        TOV = statline[16].get_text()

        return {
            'FG': FG,
            'FGA': FGA,
            'FGpercent': FGpercent,
            'threeP': threeP,
            'threePA': threePA,
            'threePpercent': threePpercent,
            'FT': FT,
            'FTA': FTA,
            'FTpercent': FTpercent,
            'ORB': ORB,
            'TRB': TRB,
            'TOV': TOV
        }
    
    def get_player_stats(self, boxscore):
        player_stats_location = boxscore.find('tbody')
        player_statlines = player_stats_location.find_all('tr')
        del player_statlines[5]

        leader_stats = {
        "PTS": {"value": 0, "name": "", "mp": 0},
        "TRB": {"value": 0, "name": "", "mp": 0},
        "AST": {"value": 0, "name": "", "mp": 0},
        "STL": {"value": 0, "name": "", "mp": 0},
        "BLK": {"value": 0, "name": "", "mp": 0},
        }

        for player in player_statlines:
            player_name = player.find('a').get_text()
            player_name = player_name.encode('iso-8859-1').decode('utf-8')
            player_stats = player.find_all('td', class_='right')
            if len(player_stats) > 10:
                stats = {
                        "TRB": int(player_stats[12].get_text()),
                        "AST": int(player_stats[13].get_text()),
                        "STL": int(player_stats[14].get_text()),
                        "BLK": int(player_stats[15].get_text()),
                        "PTS": int(player_stats[18].get_text()),
                        "MP": float(player_stats[0].get_text().split(':')[0]) + float(player_stats[0].get_text().split(':')[1]) / 60
                        }

                for stat in ["TRB", "AST", "STL", "BLK", "PTS"]:
                        if (stats[stat] > leader_stats[stat]["value"]) or (stats[stat] == leader_stats[stat]["value"] and stats["MP"] < leader_stats[stat]["mp"]):
                                leader_stats[stat] = {"value": stats[stat], "name": player_name, "mp": stats["MP"]}

        return leader_stats

    def get_stats(self, boxscores, team):
        team_abrv = self.city_to_abrv(team)
        boxscore = boxscores.find('div', id='all_box-' + team_abrv + '-game-basic')
        
        team_stats = self.get_team_stats(boxscore)
        player_stats = self.get_player_stats(boxscore)

        return {
            'team_stats': team_stats,
            'player_stats': player_stats
        }
        
    def get_boxscore_data(self, game, winner, loser):
        links = game.find('p', class_='links')
        boxscore_link = links.find('a').get('href')
        boxscore_url = website + boxscore_link
        soup = self.get_soup(boxscore_url)
        boxscores = soup.find('div', id='content')
        winner_stats = self.get_stats(boxscores, winner)
        loser_stats = self.get_stats(boxscores, loser)

        return {
            'winner': winner_stats,
            'loser': loser_stats
        }
        
    def summarize_game_info(self, games):
        game_info = []
        for game in games:
            winner_location = game.find('tr', class_='winner')
            winner = winner_location.find('a').get_text()
            winner_score = winner_location.find('td', class_='right').get_text()
            loser_location = game.find('tr', class_='loser')
            loser = loser_location.find('a').get_text()
            loser_score = loser_location.find('td', class_='right').get_text()
            OT = winner_location.find_all('td', class_='right')
            close_game = self.is_close_game(winner_score, loser_score, OT)
            boxscore_data = self.get_boxscore_data(game, winner, loser)
            game_info_dict = { "winner": {"team": winner, "score": winner_score, 
                                        "stats": boxscore_data['winner']},
                                "loser": {"team": loser, "score": loser_score,
                                        "stats": boxscore_data['loser']},
                                "close_game": close_game}

            game_info.append(game_info_dict)

        return game_info
    
    def get_recent_games(self):
        url = website + '/boxscores/'
        soup = self.get_soup(url)
        recent_games = soup.find('div', id='content')
        game_summaries = recent_games.find('div', class_='game_summaries')
        games = game_summaries.find_all('div', class_='game_summary expanded nohover')
        game_info = self.summarize_game_info(games)

        return game_info
    
    def get_offensive_and_defensive_ratings(self):
        ratings_url = website + '/leagues/NBA_2024_ratings.html'
        soup = self.get_soup(ratings_url)
        ratings_location = soup.find('div', id='div_ratings')
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
    
    def get_conference_standings(self, standings, offensive_and_defensive_ratings):
        team_standings = []

        conf_teams = standings.find_all('tr', class_='full_table')

        for team in conf_teams:
                team_name = team.find('a').get_text()
                team_record = team.find_all('td', class_='right')
                team_wins = team_record[0].get_text()
                team_losses = team_record[1].get_text()
                team_WL_pct = team_record[2].get_text()

                team_ORtg = offensive_and_defensive_ratings[team_name][0]
                team_DRtg = offensive_and_defensive_ratings[team_name][1]

                thisdict = {"team": team_name, "wins": team_wins, "losses": team_losses, "WL_pct": team_WL_pct, "ORtg": team_ORtg, "DRtg": team_DRtg}

                team_standings.append(thisdict)

        return team_standings
    
    def summarize_standings(self, standings_location):
        east_standings = standings_location.find('table', id='confs_standings_E')
        west_standings = standings_location.find('table', id='confs_standings_W')
        
        offensive_and_defensive_ratings = self.get_offensive_and_defensive_ratings()

        east_team_standings = self.get_conference_standings(east_standings, offensive_and_defensive_ratings)
        west_team_standings = self.get_conference_standings(west_standings, offensive_and_defensive_ratings)

        return [east_team_standings, west_team_standings]

    def get_standings(self):
        url = website + '/boxscores/'
        soup = self.get_soup(url)
        content = soup.find('div', id='content')
        standings_location = content.find('div', class_='standings_confs data_grid section_wrapper')
        standings = self.summarize_standings(standings_location)

        return standings
    
    def get_top_twenty_leaders(self, leaders_location):
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
    
    def get_stat_leaders(self):
        stat_leaders_url = website + '/leagues/NBA_2024_leaders.html'
        stat_leaders_soup = self.get_soup(stat_leaders_url)
        stat_location = stat_leaders_soup.find('div', id='content')
        stat_leaders_location= stat_location.find('div', class_='data_grid')


        ppg_leaders_location = stat_leaders_location.find('div', id='leaders_pts_per_g')
        rpg_leaders_location = stat_leaders_location.find('div', id='leaders_trb_per_g')
        apg_leaders_location = stat_leaders_location.find('div', id='leaders_ast_per_g')
        spg_leaders_location = stat_leaders_location.find('div', id='leaders_stl_per_g')
        bpg_leaders_location = stat_leaders_location.find('div', id='leaders_blk_per_g')
        fg3_pct_leaders_location = stat_leaders_location.find('div', id='leaders_fg3_pct')
        bpm_leaders_location = stat_leaders_location.find('div', id='leaders_bpm')

        ppg_leaders = self.get_top_twenty_leaders(ppg_leaders_location)
        rpg_leaders = self.get_top_twenty_leaders(rpg_leaders_location)
        apg_leaders = self.get_top_twenty_leaders(apg_leaders_location)
        spg_leaders = self.get_top_twenty_leaders(spg_leaders_location)
        bpg_leaders = self.get_top_twenty_leaders(bpg_leaders_location)
        fg3_pct_leaders = self.get_top_twenty_leaders(fg3_pct_leaders_location)
        bpm_leaders = self.get_top_twenty_leaders(bpm_leaders_location)

        return {"PPG": ppg_leaders, "RPG": rpg_leaders, "APG": apg_leaders, "SPG": spg_leaders, "BPG": bpg_leaders, "FG3%": fg3_pct_leaders, "BPM": bpm_leaders}

get_data()