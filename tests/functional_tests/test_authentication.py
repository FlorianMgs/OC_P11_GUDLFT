from tests.unit_tests.server.fixtures import test_club, test_comp
import server
from server import create_app
from flask import url_for
import pytest
import socket
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
def chrome_options(chrome_options):
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = 'tests/functional_tests/chromedriver.exe'
    return chrome_options


@pytest.fixture(scope="session")
def flask_port():
    # Ask OS for a free port.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session", autouse=True)
def live_server(flask_port):
    env = os.environ.copy()
    env["FLASK_APP"] = "main"
    server = subprocess.Popen(['flask', 'run', '--port', str(flask_port)], env=env)
    try:
        yield server
    finally:
        server.terminate()


class TestAuthentication:

    def test_auth(self, live_server, chrome_options, selenium):
        selenium.get(url_for('index'))
        time.sleep(50)

