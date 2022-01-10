from tests.unit_tests.server.fixtures import client, test_club


def test_authentication(client):
    """
    Authentication test: should return summary page with email in it
    """
    club = test_club()[0]
    response = client.post('/showSummary', data={'email': club['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert f"Welcome, {club['email']}" in response.data.decode()
