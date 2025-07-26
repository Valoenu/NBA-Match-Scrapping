# Import necessary libraries
import pandas as pd
from bs4 import BeautifulSoup
import os

# Get all scrapped scores from folder
directory_score = 'new_data/scores'
score_box = [os.path.join(directory_score, file) for file in os.listdir(directory_score) if file.endswith('.html')]

# This function will parse html
def html_parse(file_path):
    with open(file_path, encoding='utf-8') as file:
        html = file.read()  # read file

    soup = BeautifulSoup(html, 'html.parser')
    [selects.decompose() for selects in soup.select('tr.over_header')]  # select element to delete, i want only score box table, return a list so you have to make list comprehension
    [selects.decompose() for selects in soup.select('tr.thead')]        # Middle unnecessary line in the table
    return soup

# This function will return info about season
def info_season(soup):
    nav = soup.select('#bottom_nav_container')[0]  # Read the information for html
    links = [anchor['href'] for anchor in nav.find_all('a')]  # anchor ~ a tag in html
    season = os.path.basename(links[1]).split('_')[0]
    return season

# Read score line from parsed HTML
def line_score_reading(soup):
    score_line = pd.read_html(str(soup), attrs={'id': 'line_score'})[0]  # attrs - attribute that i wanna look from the html elements, [0] get first index

    columns = list(score_line.columns)  # fixing columns 
    columns[-1] = "total"  # Last column name
    columns[0] = "team"  # First column name
    score_line.columns = columns

    score_line = score_line[['team', 'total']]  # Select only two columns
    return score_line

# Read team statistics
def read_statistics(soup, stat, team):
    dataframe = pd.read_html(str(soup), attrs={'id': f'box-{team}-game-{stat}'}, index_col=0)[0]  # index at zero because it will return a list
    dataframe = dataframe.apply(pd.to_numeric, errors="coerce")  # Preparing data to machine learning, it cannot take string
    return dataframe

# Initialize data processing
columns_base = None  # base columns                    
list_of_games = []

# Iterate over all box score HTML files
for box_path in score_box:
    soup = html_parse(box_path)
    score_line = line_score_reading(soup)
    teams = list(score_line['team'])  # get the team names

    summaries = []  # contains a list of summary for both teams that play the game

    for team in teams:
        ''' this will create summary for specific team '''
        # specify advanced and basic stats
        advanced = read_statistics(soup, 'advanced', team)
        basic = read_statistics(soup, 'basic', team)

        maxes = pd.concat([advanced.iloc[:-1, :].max(), basic.iloc[:-1, :].max()])  # select all the rows except the last one
        maxes.index = maxes.index.str.lower() + "_max"  # convert into lower case and add -max to the name

        total = pd.concat([advanced.iloc[-1, :], basic.iloc[-1, :]])  # select the last row
        total.index = total.index.str.lower()  # convert to lower case

        summary = pd.concat([total, maxes])

        if columns_base is None:
            columns_base = list(summary.index.drop_duplicates(keep='first'))
            columns_base = [base for base in columns_base if 'bpm' not in base]  # drop 'bpm' column and duplicated columns

        summary = summary[columns_base]
        summaries.append(summary)

    summary_df = pd.concat(summaries, axis=1).T  # .T more logical way to look at it

    game = pd.concat([summary_df, score_line], axis=1)  # Add a few columns

    game['home'] = [0, 1]  # First team is away, second is home
    opponent_game = game.iloc[::-1].reset_index(drop=True)  # Reverse rows and reset index to help concatenate later

    opponent_game.columns = opponent_game.columns + '_opponent'  # Add '_opponent' suffix

    game_full = pd.concat([game, opponent_game], axis=1)

    game_full['season'] = info_season(soup)

    # Get the full game date, convert into pandas datetime and format into years, months and days
    game_full['date'] = os.path.basename(box_path)[:8]
    game_full['date'] = pd.to_datetime(game_full['date'], format='%Y%m%d')

    # Who won the game?
    game_full['won'] = game_full['total'] > game_full['total_opponent']

    list_of_games.append(game_full)

    if len(list_of_games) % 100 == 0:
        print(f'{len(list_of_games)} / {len(score_box)}')

# Combine all games into one DataFrame
games_dataframe = pd.concat(list_of_games, ignore_index=True)

# Export to CSV
games_dataframe.to_csv('NBA_Games_2025.csv')