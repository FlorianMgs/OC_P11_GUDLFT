from tests.unit_tests.server.fixtures import client, test_club


def test_points_display_without_login(client):
    response = client.get('/pointsDisplay')
    assert response.status_code == 200


def test_points_display_with_login(client, test_club):
    """
    Login first then check points display
    """
    response = client.post('/showSummary', data={'email': test_club['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Welcome, ' + test_club['email'] in response.data.decode()
    response = client.get('/pointsDisplay')
    assert response.status_code == 200
