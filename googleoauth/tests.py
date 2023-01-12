from rest_framework.test import APIClient, APITestCase
from rest_framework import status

# Create your tests here.
class GoogleOAuthApiTestCase(APITestCase):
    client = APIClient()
    correct_code_for_test = (
        "4/0AWgavdfl7luI6HRtKyme0A0ere9qjDNkgEmDL8BCSsyXZVTjQgjM4i9hWb-7ongvHf9Fuw"
    )
    wrong_code_for_test = (
        "4/0AWgavdcVuVl5orynaU-gZZZEJdx2jgHNpXjtxlTRvv-10BtlL5q07CUimmcsL2JEGAAAAA"
    )
    google_sign_in_url = "http://localhost:8000/googleoauth/v1/auth/login/google/"

    def test_get_method(self):
        resp = self.client.get(self.google_sign_in_url)
        self.assertContains(
            resp,
            text="Failed to obtain code from Google API for getting access token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

        resp = self.client.get(self.google_sign_in_url + "?error=something")
        self.assertContains(
            resp, text="something", status_code=status.HTTP_401_UNAUTHORIZED
        )

        # resp = self.client.get(self.google_sign_in_url + "?code=" + self.correct_code_for_test)
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # resp = self.client.get(self.google_sign_in_url + "?code=" + self.wrong_code_for_test)
        # self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
