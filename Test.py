from bs4 import BeautifulSoup 
import requests


website = 'https://www.basketball-reference.com/boxscores/'
result = requests.get(website)
site_content= result.text
soup = BeautifulSoup(site_content, 'html.parser')

content = soup.find('div', id='content')
game_summaries = content.find('div', class_='game_summaries')
standings = content.find('div', class_='standings_confs data_grid section_wrapper')
east_standings = standings.find('table', class_='suppress_all sortable stats_table now_sortable sticky_table eq1 re1 le1')

games = game_summaries.find_all('div', class_='game_summary expanded nohover')

print('Number of games:', len(games))

print(games[0])



# title = subbox3.find('span').get_text()
