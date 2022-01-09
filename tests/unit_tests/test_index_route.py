from tests.unit_tests.fixtures import client


def test_index_route_should_return_index_page(client):
    """
    GET request to '/' should return index page.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert "Registration Portal" in response.data.decode()
