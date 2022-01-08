from tests.unit_tests.fixtures import client


class TestPurchasePlace:

    def test_valid_points_should_book(self, client):
        """
        Valid points entry should book successful and return summary page.
        """
        club = "Simply Lift"
        competition = "Spring Festival"
        places = "1"
        response = client.post(
            '/purchasePlaces',
            data={
                'club': club,
                'competition': competition,
                'places': places
            }
        )
        assert response.status_code == 200
        assert 'booking complete' in response.data.decode()

    def test_invalid_points_should_redirect_with_error(self, client):
        """
        Invalid points should redirect to book route and display error message
        """
        club = "Simply Lift"
        competition = "Spring Festival"
        places = ["0", "-1", "1000"]

        for value in places:
            response = client.post(
                '/purchasePlaces',
                data={
                    'club': club,
                    'competition': competition,
                    'places': value
                },
                follow_redirects=True
            )
            assert response.status_code == 200
            assert 'error' in response.data.decode()

