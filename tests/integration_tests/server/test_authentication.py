from tests.unit_tests.server.fixtures import client, test_club


def test_authentication(client, test_club):
    """
    Authentication test: should return summary page with email in it
    """
    response = client.post('/showSummary', data={'email': test_club['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Welcome, ' + test_club['email'] in response.data.decode()
