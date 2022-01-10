import pytest
import server
from server import create_app
from utils import read


def test_club():
    return read('clubs.json', 'clubs')


def test_comp():
    return read('competitions.json', 'competitions')


def test_past_comp():
    return read('competitions.json', 'competitions')


@pytest.fixture
def client(mocker):
    mocker.patch.object(server, "COMPETITIONS", test_comp())
    mocker.patch.object(server, "CLUBS", test_club())
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


