from tests.unit_tests.fixtures import client, test_club


def test_points_page_should_display(client):
    response = client.get('/pointsDisplay')
    assert response.status_code == 200


def test_correct_points_should_display(client, test_club):
    """
    Check if correct clubs/amounts of points displays correctly
    """
    response = client.get('/pointsDisplay')
    assert response.status_code == 200
    assert test_club['name'] in response.data.decode()
    assert test_club['points'] in response.data.decode()
