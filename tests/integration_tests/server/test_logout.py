from tests.unit_tests.server.fixtures import client, test_club, app, captured_templates


def test_logout(client, captured_templates):
    """
    We first login, then logout and assert that we are on index page
    """
    club = test_club()[0]
    response = client.post('/showSummary', data={'email': club['email']})
    assert response.status_code == 200
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    template, context = captured_templates[1]
    assert template.name == "index.html"

