from tests.unit_tests.server.fixtures import client, app, test_club, test_comp, captured_templates


class TestBooking:

    club = test_club()[0]
    comp = test_comp()[2]

    @staticmethod
    def assert_response(response, captured_templates):

        assert response.status_code == 200
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == "welcome.html"
        assert "error" in response.data.decode()

    def test_valid_comp_valid_club_should_return_booking_page(self, client, captured_templates):
        """
        POST Data:
        club: valid
        comp: valid

        Should return:
        Booking page with success message
        """
        response = client.get(f"/book/{self.comp['name']}/{self.club['name']}")
        assert response.status_code == 200
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == "booking.html"
        assert f"Booking for {self.comp['name']}" in response.data.decode()

    def test_invalid_comp_valid_club_should_return_summary_page_with_error(self, client, captured_templates):
        """
        POST Data:
        club: valid
        comp: invalid

        Should return:
        Summary page with error message
        """
        response = client.get(f"/book/invalid_comp/{self.club['name']}")
        self.assert_response(response, captured_templates)

    def test_valid_comp_invalid_club_should_return_summary_page_with_error(self, client, captured_templates):
        """
        POST Data:
        club: invalid
        comp: valid

        Should return:
        Summary page with error message
        """
        response = client.get(f"/book/{self.comp['name']}/invalid_club")
        self.assert_response(response, captured_templates)

    def test_invalid_comp_invalid_club_should_return_summary_page_with_error(self, client, captured_templates):
        """
        POST Data:
        club: invalid
        comp: invalid

        Should return:
        Summary page with error message
        """
        response = client.get('/book/invalid_comp/invalid_club')
        self.assert_response(response, captured_templates)
