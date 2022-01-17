import json
from datetime import datetime


def read(file, data_type):
    with open(file) as f:
        data = json.load(f)[data_type]
        return data


def update_points(points: str, places: str, resas: str, club_idx: int, comp_idx: int, comp_name: str):

    with open('clubs.json') as f:
        data = json.load(f)
        data['clubs'][club_idx]['points'] = points
        data['clubs'][club_idx]['reservations'][comp_name] = resas
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


def check_points(placesRequired: int, comp: dict, club: dict) -> bool:
    # If club has already reserved 12 places on competition:
    if int(club['reservations'][comp['name']]) >= 12:
        return False
    
    # If places required are not in interval 0 - 12
    # or places required * 3 is greater than club's points
    # or places required greater than nb of places left
    if not 0 < placesRequired <= 12 or placesRequired * 3 > int(club['points']) or placesRequired > int(
        comp['numberOfPlaces']):
        return False
    else:
        return True
