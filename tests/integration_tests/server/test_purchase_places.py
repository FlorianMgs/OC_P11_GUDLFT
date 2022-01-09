from tests.unit_tests.server.fixtures import client, test_club, test_comp


def test_purchase_places(client, test_club, test_comp):
    """
    check if we can successfully purchase places after login
    """

    # login
    response = client.post('/showSummary', data={'email': test_club['email']}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Welcome, ' + test_club['email'] in response.data.decode()

    # purchasing
    response = client.post(
        '/purchasePlaces',
        data={
            'club': test_club['name'],
            'competition': test_comp['name'],
            'places': "1"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "booking complete" in response.data.decode()
