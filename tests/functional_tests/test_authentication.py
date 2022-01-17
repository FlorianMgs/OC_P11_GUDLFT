from tests.unit_tests.server.fixtures import test_club, test_comp
import server
from server import create_app
from flask import url_for
import pytest
import subprocess
import os
import time


@pytest.fixture(scope="session")
def app(session_mocker):
    session_mocker.patch.object(server, "COMPETITIONS", test_comp())
    session_mocker.patch.object(server, "CLUBS", test_club())
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')
    firefox_options.add_argument("--disable-extensions")
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--remote-debugging-port=5000")
    firefox_options.binary_location = 'tests/functional_tests/geckodriver.exe'
    return firefox_options


@pytest.fixture(scope="session", autouse=True)
def live_server():
    env = os.environ.copy()
    env["FLASK_APP"] = "main"
    server = subprocess.Popen(['flask', 'run', '--port', "5000"], env=env)
    try:
        yield server
    finally:
        server.terminate()


class TestAuthentication:

    def test_auth(self, live_server, firefox_options, selenium):
        selenium.get(url_for('index'))
        time.sleep(50)

