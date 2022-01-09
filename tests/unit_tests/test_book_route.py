from tests.unit_tests.fixtures import client, test_club, test_comp


class TestBooking:

    @staticmethod
    def assert_invalid(response):
        assert response.status_code == 200
        assert "Summary" in response.data.decode()
        assert "error" in response.data.decode()

    def test_valid_comp_valid_club_should_return_booking_page(self, client, test_club, test_comp):
        response = client.get('/book/' + test_comp['name'] + '/' + test_club['name'])
        assert response.status_code == 200
        assert "Booking for " + test_comp['name'] in response.data.decode()

    def test_invalid_comp_valid_club_should_return_summary_page_with_error(self, client, test_club, test_comp):
        response = client.get('/book/invalid_comp/' + test_club['name'])
        self.assert_invalid(response)

    def test_valid_comp_invalid_club_should_return_summary_page_with_error(self, client, test_club, test_comp):
        response = client.get('/book/' + test_comp['name'] + '/invalid_club')
        self.assert_invalid(response)

    def test_invalid_comp_invalid_club_should_return_summary_page_with_error(self, client, test_club, test_comp):
        response = client.get('/book/invalid_comp/invalid_club')
        self.assert_invalid(response)
