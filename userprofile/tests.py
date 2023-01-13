import json

import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class UserProfileTest(APITestCase):
    client = APIClient()
    baseUrl = "http://localhost:8000/"
    user = None

    def setUp(self) -> None:
        self.user = User(
            username="admin",
            password="admin",
            email="admin@gmail.com",
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        self.user.save()

    def test_sample(self):
        # try:
        #     assert 1==2
        # except AssertionError:
        #     print("Something wrong")
        assert (
            1 == 1
        )  # without catching raised error, unittest will show the error by failure. We should use this. Do not use try...catch...

    # def test_using_unittest_methods(self):
    #     with self.assertNumQueries(1):
    #         User.objects.get(email="admin@gmail.com")

    #     self.assertEqual(1,2,"something wrong")
    def test_invalid_access_to_get_method(self):
        self.assertContains(
            response=self.client.get(self.baseUrl + "user-profile/"),
            status_code=status.HTTP_401_UNAUTHORIZED,
            text="Authentication credentials were not provided",
        )

    def test_get_userprofile(self):
        # res = requests.post(
        #     self.baseUrl + "token/", json={"username": "admin", "password": "admin"}
        # )
        # print("Bearer " + res.json()["access"])
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token)
        )
        json_data = {
            "username": "admin",
            "date_of_birth": {"day": 26, "month": 5, "year": 1982},
        }
        #  https://stackoverflow.com/questions/59919695/get-body-is-not-being-sent-with-apiclient-django-drf
        resp = self.client.generic(
            method="GET",
            path=self.baseUrl + "user-profile/",
            data=json.dumps(json_data),
            content_type="application/json",
        )

        self.assertContains(
            response=resp,
            status_code=status.HTTP_200_OK,
            text="This is your profile",
        )

    def tearDown(self) -> None:
        pass
