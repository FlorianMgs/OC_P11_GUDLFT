from tests.unit_tests.server.fixtures import client, test_club


def test_points_page_should_display(client):
    response = client.get('/pointsDisplay')
    assert response.status_code == 200


def test_correct_points_should_display(client):
    """
    Check if correct clubs/amounts of points displays correctly
    """
    club = test_club()[0]
    response = client.get('/pointsDisplay')
    assert response.status_code == 200
    assert club['name'] in response.data.decode()
    assert club['points'] in response.data.decode()
