from parse_brackets import load_538_predictions, main
import requests
ACTUAL_ROUND_DICT = {'Duke': 4, 'North Dakota St': 1, 'VCU': 1, 'UCF': 2, 'Mississippi St': 1, 'Liberty': 2,
                     'Virginia Tech': 3, 'Saint Louis': 1, 'Maryland': 2, 'Belmont': 1, 'LSU': 3, 'Yale': 1,
                     'Louisville': 1, 'Minnesota': 2, 'Michigan State': 5, 'Bradley': 1,

                     'Gonzaga': 4, 'F. Dickinson': 1, 'Syracuse': 1, 'Baylor': 2, 'Marquette': 1, 'Murray State': 2,
                     'Florida St': 3, 'Vermont': 1, 'Buffalo': 2, 'Arizona State': 1, 'Texas Tech': 6, 'N Kentucky': 1,
                     'Nevada': 1, 'Florida': 2, 'Michigan': 3, 'Montana': 1,

                     'Virginia': 7, 'Gardner-Webb': 1, 'Ole Miss': 1, 'Oklahoma': 2, 'Wisconsin': 1, 'Oregon': 3,
                     'Kansas State': 1, 'UC Irvine': 2, 'Villanova': 2, "Saint Mary's": 1,
                     'Purdue': 4, 'Old Dominion': 1, 'Cincinnati': 1, 'Iowa': 2, 'Tennessee': 3, 'Colgate': 1,

                     'North Carolina': 3, 'Iona': 1, 'Utah State': 1, 'Washington': 2,
                     'Auburn': 5, 'New Mexico St': 1, 'Kansas': 2, 'Northeastern': 1, 'Iowa State': 1, 'Ohio State': 2,
                     'Houston': 3, 'Georgia State': 1, 'Wofford': 2, 'Seton Hall': 1, 'Kentucky': 4, 'Abil Christian': 1}


PROBABILITIES = load_538_predictions()
#FILL IN WITH ACTUAL STARTING 538 PROBABILITIES {key: team name, value: [None, make round1 prob, make round2 prob, etc.]}
ROUND_MULTIPLIERS = [None, 1, 2, 4, 8, 16, 32] #None to 1-index round numbers
base_url = "http://fantasy.espn.com/tournament-challenge-bracket/2019/en/entry?entryID="
entry_ids = {"Kevin": "24753605", "Varun": "21291058", "Chris": "18889789", "Mike": "23669559",
             "George": "28781895", "Dennis": "33559396", "Leo": "28990005"}

# modified scoring
for entry in entry_ids:
    score = 0
    response = requests.get(base_url + entry_ids[entry]).text
    main(response)
    with open("predictions.txt") as f: #f is txt file with each line being TEAM_NAME PREDICTED_ROUND space seperated
        for line in f.readlines():
            data = line.strip().split()
            team, predicted_round = ' '.join(data[:-1]), int(data[-1])
            actual_round = ACTUAL_ROUND_DICT[team]
            for r in range(1, min(predicted_round, actual_round) + 1):
                score += 1 / PROBABILITIES[team][r] * ROUND_MULTIPLIERS[r]
    print(str(score) + ' ' + entry)

# traditional scoring to check accuracy
for entry in entry_ids:
    score = 0
    response = requests.get(base_url + entry_ids[entry]).text
    main(response)
    with open("predictions.txt") as f: #f is txt file with each line being TEAM_NAME PREDICTED_ROUND space seperated
        for line in f.readlines():
            data = line.strip().split()
            team, predicted_round = ' '.join(data[:-1]), int(data[-1])
            actual_round = ACTUAL_ROUND_DICT[team]
            for r in range(1, min(predicted_round, actual_round)):
                score += 10 * ROUND_MULTIPLIERS[r]
    print(str(score) + ' ' + entry)