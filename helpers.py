import json
from datetime import datetime


def read(file, data_type):
    with open(file) as f:
        data = json.load(f)[data_type]
        return data


def update_points(points: str, places: str, club_idx: int, comp_idx=int):

    with open('clubs.json') as f:
        data = json.load(f)
        data['clubs'][club_idx]['points'] = points
        json.dump(data, open('clubs.json', 'w'), indent=4)

    with open('competitions.json') as f:
        data = json.load(f)
        data['competitions'][comp_idx]['numberOfPlaces'] = places
        json.dump(data, open('competitions.json', 'w'), indent=4)


def update_competition_dict_with_past_bool(competitions: list) -> list:
    updated_comp = []
    for comp in competitions:
        try:
            if datetime.now() > datetime.strptime(comp["date"][2:], '%y-%m-%d %H:%M:%S'):
                comp["past"] = True
                updated_comp.append(comp)
            else:
                updated_comp.append(comp)
        except ValueError:
            updated_comp.append(comp)
    return updated_comp
