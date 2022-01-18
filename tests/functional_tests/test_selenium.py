from tests.unit_tests.server.fixtures import test_club, test_comp
from selenium.webdriver.common.keys import Keys
import server
from server import create_app
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
    firefox_options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
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
        selenium.get('http://127.0.0.1:5000/')
        email_input = selenium.find_element_by_id('email')
        email_input.send_keys(test_club()[0]['email'], Keys.ENTER)
        time.sleep(1)
        selenium.close()

    def test_logout(self, live_server, firefox_options, selenium):
        # login first
        selenium.get('http://127.0.0.1:5000/')
        email_input = selenium.find_element_by_id('email')
        email_input.send_keys(test_club()[0]['email'], Keys.ENTER)
        time.sleep(1)
        # then logout
        selenium.find_element_by_id('logout').click()
        time.sleep(1)
        selenium.close()

    def test_points_display_logged_out_and_logged_in(self, live_server, firefox_options, selenium):
        # Logged out first
        selenium.get('http://127.0.0.1:5000/')
        selenium.find_element_by_id('points_display').click()
        time.sleep(1)
        selenium.find_element_by_id('back').click()

        # Now we log in and go to points display page through welcome.html
        email_input = selenium.find_element_by_id('email')
        email_input.send_keys(test_club()[0]['email'], Keys.ENTER)
        time.sleep(1)
        selenium.find_element_by_id('points_display').click()
        time.sleep(1)
        selenium.find_element_by_id('back').click()
        selenium.close()

    def test_purchase_places(self, live_server, firefox_options, selenium):
        # login first
        selenium.get('http://127.0.0.1:5000/')
        email_input = selenium.find_element_by_id('email')
        email_input.send_keys(test_club()[0]['email'], Keys.ENTER)
        time.sleep(1)

        # navigate to booking page
        selenium.find_elements_by_xpath("//a[contains(text(),'Book')]")[0].click()
        time.sleep(1)
        selenium.find_element_by_id('places_no').send_keys('1', Keys.ENTER)
        time.sleep(2)



