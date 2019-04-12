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
    teams = [team for index, team in load_team_indices(response).items()]

    with open('538', 'r') as f:
        fivethirtyeight_predictions = f.read()
    probabilities = {}
    for team in teams:
        start_index = fivethirtyeight_predictions.find('\n', fivethirtyeight_predictions.find(team)) + 1
        round_probabilites = [None]
        for i in range(0, 6):
            end_index = fivethirtyeight_predictions.find('\n', start_index) + 1
            probability = fivethirtyeight_predictions[start_index:end_index]
            if probability == '<0.1%\n':
                round_probabilites.append(.005)
            else:
                round_probabilites.append(float(probability.strip('%\n'))/ 100)
            start_index = end_index
        probabilities[team] = round_probabilites
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
    round_to_advance_to = {}
    for i in range(0, 32):
        round_to_advance_to[team_indices[picks[i]]] = 2
    for i in range(32, 48):
        round_to_advance_to[team_indices[picks[i]]] = 3
    for i in range(48, 56):
        round_to_advance_to[team_indices[picks[i]]] = 4
    for i in range(56, 60):
        round_to_advance_to[team_indices[picks[i]]] = 5
    for i in range(60, 62):
        round_to_advance_to[team_indices[picks[i]]] = 6
    for i in range(62, 63):
        round_to_advance_to[team_indices[picks[i]]] = 7
    for team_index, team in team_indices.items():
        if team not in round_to_advance_to:
            round_to_advance_to[team] = 1
    with open('predictions.txt', 'w') as f:
        for team, pick in round_to_advance_to.items():
            f.write(team + ' ' + str(pick) + '\n')

