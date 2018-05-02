import json
import os

import dota2api

from config import *

def load_json(file_name):
    if os.path.exists(file_name):
        with open(file_name) as json_data:
            d = json.load(json_data)
            return d
    else:
        return {}


def write_json(file_name, json_data):
    print('writting:' + file_name)
    with open(file_name, 'w') as outfile:
        json.dump(json_data, outfile)


def get_leagues():
    api = dota2api.Initialise(API_KEY)
    leagues = api.get_league_listing()['leagues']
    write_json("data/leagues.json", leagues)
    for league in leagues:
        file_path = "data/leagues/" + str(league['leagueid']) + ".json"
        if not os.path.exists(file_path):
            # if league['leagueid'] == 1640:
            data = {}
            league_data = api.get_match_history(league_id=league['leagueid'],
                                                matches_requested=100, tournament_games_only='1')
            while league_data['results_remaining'] > 0:
                print(league_data['total_results'])
                print(league_data['results_remaining'])
                for match in league_data['matches']:
                    match['detail'] = api.get_match_details(match_id=match['match_id'])
                data.update({m['match_id']: m for m in league_data['matches']})
                league_data = api.get_match_history(league_id=league['leagueid'],
                                                    start_at_match_id=league_data['matches'][-1]['match_id'],
                                                    matches_requested=100, tournament_games_only='1')
            write_json(file_path, data)


if __name__ == '__main__':
    get_leagues()
