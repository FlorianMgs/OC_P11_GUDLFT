from locust import HttpUser, task
#from tests.unit_tests.server.fixtures import test_club, test_comp


class ProjectperfTest(HttpUser):

    # club = test_club()[0]
    # comp = test_comp()[2]

    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post('/showSummary', {'email': 'john@simplylift.co'})

    @task
    def purchase_points(self):
        # mocker.patch.object(server, "COMPETITIONS", test_comp())
        # mocker.patch.object(server, "CLUBS", test_club())
        self.client.post(
            '/purchasePlaces',
            {
                'club': "Simply Lift",
                'competition': 'Summer Festival 2022',
                'places': "1"
            }
        )


