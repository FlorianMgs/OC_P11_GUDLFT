from tests.unit_tests.server.fixtures import client, test_club


def test_logout(client, test_club):
    """
    We first login, then logout and assert that we are on index page
    """
    response = client.post('/showSummary', data={'email': test_club['email']})
    assert response.status_code == 200
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert "GUDLFT Registration" in response.data.decode()
