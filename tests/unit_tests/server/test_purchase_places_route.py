from tests.unit_tests.server.fixtures import client, app, captured_templates


class TestPurchasePlace:

    @staticmethod
    def get_response(client, club, comp, points):
        return client.post(
            '/purchasePlaces',
            data={
                'club': club,
                'competition': comp,
                'places': points
            },
            follow_redirects=True
        )

    @staticmethod
    def assert_response(response, template_name, msg, captured_templates):
        assert response.status_code == 200
        template, context = captured_templates[0]
        assert template.name == template_name
        assert msg in response.data.decode()

    def test_valid_points_valid_club_valid_comp_should_book(self, client, captured_templates):
        """
        POST Data:
        club: valid
        comp: valid
        places: valid

        Should return:
        Summary page with success message
        """
        response = self.get_response(client, "Simply Lift", "Spring Festival", "1")
        self.assert_response(response, "welcome.html", "booking complete", captured_templates)

    def test_invalid_points_valid_club_valid_comp_should_redirect_to_summary_page_with_error(self, client, captured_templates):
        """
        Occurs only when user modify form / POST request through dev tools.
        POST Data:
        club: valid
        comp: valid
        places: invalid

        Should return:
        Booking page with error message
        """
        places = ["0", "-1", "1000", "a"]

        for value in places:
            response = self.get_response(client, "Simply Lift", "Spring Festival", value)
            self.assert_response(response, "booking.html", "error", captured_templates)

    def test_valid_points_invalid_club_valid_comp_should_redirect_to_index(self, client, captured_templates):
        """
        Occurs only when user modify form / POST request through dev tools.
        POST Data:
        club: invalid
        comp: valid
        places: valid

        Should return:
        Index page with error message
        """
        response = self.get_response(client, "InvalidClub", "Spring Festival", "1")
        self.assert_response(response, "index.html", "error", captured_templates)

    def test_valid_points_valid_club_invalid_comp_should_redirect_to_index(self, client, captured_templates):
        """
        Occurs only when user modify form / POST request through dev tools.
        POST Data:
        club: valid
        comp: invalid
        places: valid

        Should return:
        Index page with error message
        """
        response = self.get_response(client, "Simply Lift", "InvalidComp", "1")
        self.assert_response(response, "index.html", "error", captured_templates)

    def test_valid_points_invalid_club_invalid_comp_should_redirect_to_index(self, client, captured_templates):
        """
        Occurs only when user modify form / POST request through dev tools.
        POST Data:
        club: invalid
        comp: invalid
        places: valid

        Should return:
        Index page with error message
        """
        response = self.get_response(client, "InvalidClub", "InvalidComp", "1")
        self.assert_response(response, "index.html", "error", captured_templates)

    def test_invalid_points_invalid_club_invalid_comp_should_redirect_to_index(self, client, captured_templates):
        """
        Occurs only when user modify form / POST request through dev tools.
        POST Data:
        club: invalid
        comp: invalid
        places: invalid

        Should return:
        Index page with error message
        """
        response = self.get_response(client, "InvalidClub", "InvalidComp", "a")
        self.assert_response(response, "index.html", "error", captured_templates)

