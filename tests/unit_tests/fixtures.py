import pytest
from server import create_app
from helpers import read


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_club():
    return read('clubs.json', 'clubs')[0]


@pytest.fixture
def test_comp():
    return read('competitions.json', 'competitions')[2]


@pytest.fixture
def test_past_comp():
    return read('competitions.json', 'competitions')[0]
