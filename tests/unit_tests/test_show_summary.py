from tests.unit_tests.fixtures import client, test_club, test_past_comp


class TestShowSummary:

    def test_valid_email_should_return_welcome_page(self, test_club, client):
        """
        As we dont have means to assert used templates, we check if our posted email is in response
        """
        valid_email = test_club["email"]
        response = client.post('/showSummary', data={'email': valid_email})
        assert response.status_code == 200
        assert valid_email in response.data.decode()

    def test_invalid_email_should_return_index_page_with_error(self, client):
        """
        As we dont have means to assert used templates, we check if the error message is in response
        """
        invalid_email = 'invalid@simplylift.com'
        response = client.post('/showSummary', data={'email': invalid_email}, follow_redirects=True)
        assert response.status_code == 200
        assert 'error' in response.data.decode()

    def test_past_competition_should_not_be_bookable(self, test_club, test_past_comp, client):
        """
        Check if past competition is unbookable. "Past competition" should be written instead of Booking link
        """
        response = client.post('/showSummary', data={'email': test_club['email']})
        assert response.status_code == 200
        assert test_past_comp['name'] in response.data.decode() and "Past competition" in response.data.decode()


