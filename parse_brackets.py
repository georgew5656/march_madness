import requests
import json

team_key = "espn.fantasy.maxpart.config.scoreboard_teams = "
picks_key = "espn.fantasy.maxpart.config.savedPicks = '"


def zero_append(int_as_string):
    if int_as_string > 9:
        return str(int_as_string)
    else:
        return '0' + str(int_as_string)


def load_538_predictions():
    base_url = "http://fantasy.espn.com/tournament-challenge-bracket/2019/en/entry?entryID=24753605"
    response = requests.get(base_url).text
    teams = set([team for index, team in load_team_indices(response).items()])
    probabilities = {}
    with open('538', 'r') as f:
        for line in f:
            line_split = line.split(" ")
            line_split.reverse()
            predictions = line_split[:6]
            predictions.reverse()
            team = line_split[6:]
            team.reverse()
            team = ' '.join(team)
            if team not in teams:
                raise Exception()
            probabilities[team] = [0.0] + [float(x) for x in predictions]
    return probabilities
def load_team_indices(html):
    team_key_start_index = html.find(team_key) + len(team_key)
    team_key_end_index = html.find("\n", team_key_start_index) - 1
    teams = json.loads(html[team_key_start_index:team_key_end_index])
    team_indices = {}
    for team in teams:
        team_indices[zero_append(team['id'])] = team['n']
    return team_indices


def load_picks(html):
    picks_start_index = html.find(picks_key) + len(picks_key)
    picks_end_index =html.find("\n", picks_start_index) - 2
    picks = html[picks_start_index:picks_end_index].split('|')
    return picks

def main(html):
    team_indices = load_team_indices(html)
    picks = load_picks(html)
    rounds_won = {}
    for i in range(0, 32):
        rounds_won[team_indices[picks[i]]] = 1
    for i in range(32, 48):
        rounds_won[team_indices[picks[i]]] = 2
    for i in range(48, 56):
        rounds_won[team_indices[picks[i]]] = 3
    for i in range(56, 60):
        rounds_won[team_indices[picks[i]]] = 4
    for i in range(60, 62):
        rounds_won[team_indices[picks[i]]] = 5
    for i in range(62, 63):
        rounds_won[team_indices[picks[i]]] = 6
    for team_index, team in team_indices.items():
        if team not in rounds_won:
            rounds_won[team] = 0
    with open('predictions.txt', 'w') as f:
        for team, pick in rounds_won.items():
            f.write(team + ' ' + str(pick) + '\n')

