from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class FcmApiTestCase(APITestCase):
    baseUrl = "http://localhost:8000/"

    def setUp(self) -> None:
        client = APIClient()

        users = [
            ("admin", "admin", "admin@gmail.com", True),
            ("truongtronghai@gmail.com", "secret", "truongtronghai@gmail.com", False),
            ("beginningpace@gmail.com", "secret", "beginningpace@gmail.com", False),
        ]
        for i in users:
            user = User(
                username=i[0], password=i[1], email=i[2], is_active=True, is_staff=i[3]
            )
            user.save()

        # authenticate for user one time before testing
        # HERE, I don't know why we have to create access token manually. But, we MUST do that. If just creating token by calling request, authorization will be failed.
        user = User.objects.get(username="admin")
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token)
        )

    def test_fcm_call_by_non_staff_user(self):
        normal_user = User.objects.get(username="truongtronghai@gmail.com")
        refresh = RefreshToken.for_user(normal_user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token)
        )
        send_data = {
            "email": "beginningpace@gmail.com",
            "device_type": "ios",
            "registration_id": "DQZWvePdbsfyVEnXK13Q2B:BBBBBbHO5NbPn4l1FTTRLTE_FRk0i5cKFic4ix4INQHh95ZQ7tKKqosYM67ZYwmeCVSUXkvRIC1xxBslLx-WjVcAyqlqdIrLB2P5l83rlnjiPHIApLwU5Ytw7Lu1lZ9UEaW7soYkQABC",
        }

        resp = self.client.post(
            self.baseUrl + "user/device-token/", send_data, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fcm(self):
        # test user not existed
        send_data = {
            "email": "nouser@gmail.com",
            "device_type": "ios",
            "registration_id": "DQZWvePdbsfyVEnXK13Q2B:BBBBBbHO5NbPn4l1FTTRLTE_FRk0i5cKFic4ix4INQHh95ZQ7tKKqosYM67ZYwmeCVSUXkvRIC1xxBslLx-WjVcAyqlqdIrLB2P5l83rlnjiPHIApLwU5Ytw7Lu1lZ9UEaW7soYkQABC",
        }

        resp = self.client.post(
            self.baseUrl + "user/device-token/", send_data, format="json"
        )
        self.assertContains(
            resp,
            status_code=status.HTTP_400_BAD_REQUEST,
            text="User with the email does not exist",
        )

        # test successful
        send_data = {
            "email": "beginningpace@gmail.com",
            "device_type": "ios",
            "registration_id": "DQZWvePdbsfyVEnXK13Q2B:BBBBBbHO5NbPn4l1FTTRLTE_FRk0i5cKFic4ix4INQHh95ZQ7tKKqosYM67ZYwmeCVSUXkvRIC1xxBslLx-WjVcAyqlqdIrLB2P5l83rlnjiPHIApLwU5Ytw7Lu1lZ9UEaW7soYkQABC",
        }

        resp = self.client.post(
            self.baseUrl + "user/device-token/", send_data, format="json"
        )
        self.assertContains(
            resp,
            status_code=status.HTTP_200_OK,
            text="Registration ID has been created successfully",
        )
