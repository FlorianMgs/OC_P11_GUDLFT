import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_club():
    return {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "40"
    }


@pytest.fixture
def test_comp():
    return {
        "name": "Summer Festival 2022",
        "date": "2022-06-22 13:30:00",
        "numberOfPlaces": "58"
    }


@pytest.fixture
def test_past_comp():
    return {
        "name": "Summer Festival 2022",
        "date": "2020-06-22 13:30:00",
        "numberOfPlaces": "58"
    }
