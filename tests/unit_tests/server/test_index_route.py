from tests.unit_tests.server.fixtures import client, app, captured_templates


def test_index_route_should_return_index_page(client, captured_templates):
    """
    GET request to '/' should return index page.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"
