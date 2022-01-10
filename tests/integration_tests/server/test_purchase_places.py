from tests.unit_tests.server.fixtures import client, test_club, test_comp


def test_purchase_places(client):
    """
    check if we can successfully purchase places after login
    """
    club = test_club()[0]
    comp = test_comp()[2]

    # login
    response = client.post('/showSummary', data={'email': club['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert f"Welcome, {club['email']}" in response.data.decode()

    # purchasing
    response = client.post(
        '/purchasePlaces',
        data={
            'club': club['name'],
            'competition': comp['name'],
            'places': "1"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "booking complete" in response.data.decode()
