from datetime import datetime

import requests  # https://www.w3schools.com/python/module_requests.asp
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# simpleJWT
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
def get_google_oauth2_tokens(code, redirect_uri, *args):
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(settings.GOOGLE_TOKEN_URI, data)
    if not response.ok:
        return Response(
            {"detail": "Failed to obtain access token from Google."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response.json()


def get_google_profile_info(access_token=""):
    response = requests.get(
        settings.GOOGLE_GET_PROFILE_URL + "?access_token=" + access_token
    )
    if not response.ok:
        return Response(
            {"detail": "Failed to get user profile from Google."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response.json()


def get_tokens_for_user(user):
    """
    Using SimpleJWT to create tokens manually
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def google_validate_id_token(id_token=None):
    response = requests.get(
        settings.GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token}
    )
    if not response.ok:
        raise ValidationError("Google id_token is invalid.")

    # The final step to authenticate this request is by comparing the aud (short for audience) from the Google response with the GOOGLE_CLIENT_ID configured in your settings.py
    audience = response.json()["aud"]
    if audience != settings.GOOGLE_CLIENT_ID:
        return False
    return True


class GoogleAuthApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Description: check "code" from Google Auth to decide to allow user login to system. If email of user existed in system, just log in. If not, creating new one and log in. This endpoint is requested from Google consent display

        Parameter: "code" was passed to BE in query string ( GET parameters )
        """
        if request.GET.get("error") is not None:
            return Response(
                {"detail": request.GET.get("error")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # get the "code" in result of Google return
        code = request.GET.get("code")
        # print(code)
        if code is not None:
            result_tokens = get_google_oauth2_tokens(
                code=code,
                redirect_uri="http://localhost:8000/googleoauth/v1/auth/login/google/",
            )

            # print(result_tokens)
            ### Use this code snippet to get "id token" for test method post. Comment it for operating normally
            # return Response(result_tokens, status=status.HTTP_200_OK)
            ###

            google_user_profile = get_google_profile_info(
                access_token=result_tokens["access_token"]
            )
            # print(google_user_profile)
            user = None
            try:
                user = User.objects.get(email=google_user_profile["email"])
                # user.username = google_user_profile["email"]
            except User.DoesNotExist:
                # create new user with Google profile
                user = User.objects.create(
                    username=google_user_profile["email"],
                    first_name=google_user_profile.get(
                        "family_name", ""
                    ),  # if no key exists, return ""
                    last_name=google_user_profile.get("given_name", ""),
                    email=google_user_profile["email"],
                    is_active=True,
                    is_staff=False,
                    is_superuser=False,
                    last_login=datetime.now(),
                    date_joined=datetime.now(),
                )
                user.set_password("I*En!)8P9xgs*q8*")
                user.save()
            # because password has been saved in hash form, we cannot call post request to url "token_obtain_pair". We will create tokens manually by SimpleJWT
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "detail": "Failed to obtain code from Google API for getting access token"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def post(self, request, *args, **kwargs):
        """
        Description: check ID token from Google Auth to decide to allow user login to system. If email of user existed in system, just log in. If not, creating new one and log in

        Parameter: tokenID was passed to BE in "Authorization" header
        Post data: { "email": <username (email) of user in Google>}
        """
        google_auth_token_id_from_fe = request.headers.get("Authorization")

        if google_auth_token_id_from_fe is None:
            return Response(
                {"detail": "Id Token does not exist"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        try:
            if google_validate_id_token(google_auth_token_id_from_fe):
                try:
                    user = User.objects.get(email=request.data["email"])
                except User.DoesNotExist:
                    # create new user with Google profile
                    user = User.objects.create(
                        username=request.data["email"],
                        email=request.data["email"],
                        is_active=True,
                        is_staff=False,
                        is_superuser=False,
                        last_login=datetime.now(),
                        date_joined=datetime.now(),
                    )
                    user.set_password("I*En!)8P9xgs*q8*")
                    user.save()
                # because password has been saved in hash form, we cannot call post request to url "token_obtain_pair". We will create tokens manually by SimpleJWT
                tokens = get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "user login information is unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except ValidationError:
            return Response(
                {"detail": "Id Token is validated failed by Google Auth"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
