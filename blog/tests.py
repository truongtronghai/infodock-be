from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Post, Category
from rest_framework import status
import requests
from rest_framework_simplejwt.tokens import RefreshToken
import itertools
from django.utils import timezone


class BlogTest(APITestCase):
    client = APIClient()
    baseUrl = "http://localhost:8000/"

    def setUp(self) -> None:
        users = [
            ("admin", "admin", "admin@gmail.com"),
            ("truongtronghai@gmail.com", "secret", "truongtronghai@gmail.com"),
            ("beginningpace@gmail.com", "secret", "beginningpace@gmail.com"),
        ]
        for i in users:
            user = User(
                username=i[0],
                password=i[1],
                email=i[2],
                is_active=True,
                is_superuser=True,
                is_staff=True,
            )
            user.save()
        # prepare mock Category data
        for i in range(2, 10):
            category = Category(
                name="Category " + str(i), slug="cateogry-" + str(i), parent=None
            )
            category.save()

        # authenticate for user one time before testing
        # HERE, I don't know why we have to create access token manually. But, we MUST do that. If just creating token by calling request, authorization will be failed.
        user = User.objects.get(username="truongtronghai@gmail.com")
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token)
        )

        # prepare mock Post data
        for i in range(2, 10):
            category = Category.objects.get(name="Category " + str(i))
            datetime_of_now = timezone.now()
            post = Post(
                user=user,
                category=category,
                title="lorem ipsum " + str(i),
                slug="lorem-ipsum-" + str(i),
                excerpt="sample sample sample sample",
                content=itertools.repeat("sample", 30),
                created_date=datetime_of_now,
                edited_date=datetime_of_now,
            )
            post.save()

    def test_fixture_run(self):
        with self.assertNumQueries(1):
            Category.objects.get(id=1)

    def test_set_up_successfully(self):
        with self.assertNumQueries(3):
            User.objects.get(username="admin")
            User.objects.get(username="truongtronghai@gmail.com")
            User.objects.get(username="beginningpace@gmail.com")

    def test_list_categories(self):
        """
        With viewset, APIClient always return code 301. I have to use "requests" to implement test case
        """
        tokens = requests.post(
            self.baseUrl + "token/", json={"username": "admin", "password": "admin"}
        )
        resp = requests.get(
            self.baseUrl + "blog/category",
            headers={"Authorization": "Bearer " + tokens.json()["access"]},
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_retrieve_not_existed_category(self):
        tokens = requests.post(
            self.baseUrl + "token/", json={"username": "admin", "password": "admin"}
        )
        resp = requests.get(
            self.baseUrl + "blog/category/100",
            headers={"Authorization": "Bearer " + tokens.json()["access"]},
        )

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.json()["message"], "No category found")

    def test_retrieve_category(self):
        # user = User.objects.get(username="truongtronghai@gmail.com")
        # refresh = RefreshToken.for_user(user)
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        resp = self.client.get(self.baseUrl + "blog/category/1/")
        # print(resp.json()["message"])
        self.assertContains(
            resp, text="Category existed", status_code=status.HTTP_200_OK
        )

    def test_create_failed(self):
        # user = User.objects.get(username="truongtronghai@gmail.com")
        # refresh = RefreshToken.for_user(user)
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

        resp = self.client.post(
            self.baseUrl + "blog/category/",
            {"name": "hello", "slug": "hello", "parent": 99},  # not existed ID
            format="json",
        )

        self.assertContains(
            resp, text="Parent ID is not existed", status_code=status.HTTP_404_NOT_FOUND
        )

    def test_create_successfully(self):
        # user = User.objects.get(username="truongtronghai@gmail.com")
        # refresh = RefreshToken.for_user(user)
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

        category = Category.objects.get(name="Category 2")

        resp = self.client.post(
            self.baseUrl + "blog/category/",
            {"name": "hello", "slug": "hello", "parent": category.id},
            format="json",
        )
        # print(resp.json()["message"])
        self.assertContains(
            resp, text="Category created", status_code=status.HTTP_200_OK
        )

    def test_update_not_existed_category_id(self):
        resp = self.client.put(
            self.baseUrl + "blog/category/1000/",
            {"name": "New Category", "slug": "new-category", "parent": None},
            format="json",
        )
        self.assertContains(
            resp,
            text="No category found for updating",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    def test_update_no_parent_category_id(self):
        category_2 = Category.objects.get(name="Category 2")
        category_3 = Category.objects.get(name="Category 3")
        resp = self.client.put(
            self.baseUrl + "blog/category/" + str(category_2.id) + "/",
            {
                "name": "New Category",
                "slug": "new-category",
                "parent": category_3.id + 100,  # mock data
            },
            format="json",
        )
        self.assertContains(
            resp, text="Parent ID is not existed", status_code=status.HTTP_404_NOT_FOUND
        )

    def test_update_category_successfull(self):
        category_2 = Category.objects.get(name="Category 2")
        category_3 = Category.objects.get(name="Category 3")
        resp = self.client.put(
            self.baseUrl + "blog/category/" + str(category_2.id) + "/",
            {"name": "New Category", "slug": "new-category", "parent": category_3.id},
            format="json",
        )
        self.assertContains(
            resp, text="Category updated", status_code=status.HTTP_200_OK
        )

        resp = self.client.put(
            self.baseUrl + "blog/category/" + str(category_2.id) + "/",
            {"name": "New Category", "slug": "new-category", "parent": None},
            format="json",
        )
        self.assertContains(
            resp, text="Category updated", status_code=status.HTTP_200_OK
        )

    def test_delete_category_successfull(self):
        category_2 = Category.objects.get(name="Category 2")
        resp = self.client.delete(
            self.baseUrl + "blog/category/" + str(category_2.id) + "/",
            {},
            format="json",
        )
        self.assertContains(
            resp, text="Category deleted successfully", status_code=status.HTTP_200_OK
        )

    def test_delete_category_failed(self):
        category_2 = Category.objects.get(name="Category 2")
        resp = self.client.delete(
            self.baseUrl
            + "blog/category/"
            + str(category_2.id + 100)
            + "/",  # mock data for not existed category id
            {},
            format="json",
        )
        self.assertContains(
            resp,
            text="Category does not exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        resp = self.client.delete(
            self.baseUrl + "blog/category/1/",  # delete default category
            {},
            format="json",
        )
        self.assertContains(
            resp,
            text="Deleting default category is not allowed",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def test_get_detail_post(self):
        test_post = Post.objects.get(title="lorem ipsum 2")
        resp = self.client.get(self.baseUrl + "blog/" + test_post.slug + "/")
        self.assertContains(resp, text="lorem ipsum 2", status_code=status.HTTP_200_OK)

        resp = self.client.get(self.baseUrl + "blog/some-slug-for-test/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_posts(self):
        category = Category.objects.get(name="Category 2")
        resp = self.client.get(self.baseUrl + "blog/posts/" + category.slug + "/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(
            self.baseUrl + "blog/posts/" + category.slug + "/?page=1000"
        )
        self.assertContains(
            resp, text="Invalid page", status_code=status.HTTP_404_NOT_FOUND
        )

        resp = self.client.get(self.baseUrl + "blog/posts/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.client.get(self.baseUrl + "blog/posts/some-slug-for-test-wrong/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_posts(self):
        resp = self.client.get(self.baseUrl + "blog/search/lorem/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(self.baseUrl + "blog/search/lorem/?page=1000")
        self.assertContains(
            resp, text="Invalid page", status_code=status.HTTP_404_NOT_FOUND
        )
