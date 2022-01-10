import pytest
import server
from server import create_app


def test_club():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "40"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]


def test_comp():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "20"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Summer Festival 2022",
            "date": "2022-06-22 13:30:00",
            "numberOfPlaces": "23"
        }
    ]


@pytest.fixture
def client(mocker):
    mocker.patch.object(server, "COMPETITIONS", test_comp())
    mocker.patch.object(server, "CLUBS", test_club())
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


