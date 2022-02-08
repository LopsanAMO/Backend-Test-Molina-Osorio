import mock
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from corner_test.apps.menus.tests.factories import (
    DishFactory,
    MenuFactory,
    OrderFactory,
    UserFactory,
)
from corner_test.apps.employees.tests.factories import EmployeeFactory
from corner_test.apps.menus.serializers import (
    OrderSerializer,
    MenuListSerializer,
    DishSerializer,
    MenuCreateUpdateSerializer,
    SimpleDishSerializer,
)
from rest_framework.reverse import reverse
from corner_test.apps.menus.models import Menu, Dish, Order
from corner_test.apps.employees.models import Employee
from corner_test.apps.utils.tests.test_services import (
    mocked_slack_channel,
    mocked_slack_messages,
)
from corner_test.apps.utils.exceptions import SlackErrorException


class TestLoginView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}

    def test_login_credentials_ok(self):
        response = self.client.post(self.url_login, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        token = response.data["access"]
        verification_url = reverse("token_verify")
        resp = self.client.post(verification_url, {"token": token}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_login_credentails_fail(self):
        payload = {"username": "foo2", "password": "p"}
        response = self.client.post(self.url_login, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_not_active_account_credentials(self):
        user = User.objects.create_user(
            username="foo4", email="user@foo.com", password="pass", is_active=False
        )
        payload = {"username": "foo4", "password": "pass"}
        response = self.client.post(self.url_login, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestOrderListViewSet(TestCase):
    def setUp(self):
        self.url = "/api/v1/orders/"
        self.client = APIClient()
        self.menu = MenuFactory()
        self.dish = DishFactory(menu=self.menu)
        self.employee = EmployeeFactory()
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    @mock.patch("slack.WebClient.conversations_list", side_effect=mocked_slack_channel)
    @mock.patch(
        "slack.WebClient.conversations_history", side_effect=mocked_slack_messages
    )
    def test_get_request_return_order_list(self, mock_chanel, mock_messages):
        Menu.objects.get_or_create(id=99)
        Dish.objects.get_or_create(id=99, menu_id=99)
        employee, _ = Employee.objects.get_or_create(slack_user_id="FSAF2133")
        response = self.client.get(self.url)
        result = response.json()
        specifications = mocked_slack_messages()["messages"][0]["text"]
        self.assertEqual(result["results"][0]["specifications"], specifications)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_list_slack_channels_not_foundchannel_not_found(self):
        with self.assertRaises(SlackErrorException):
            response = self.client.get(self.url)
            result = response.json()


class TestMenuListViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/menus/"
        self.menu = MenuFactory(date=datetime.now())
        self.menu_2 = MenuFactory(date=datetime.now() - timedelta(days=1))
        self.dish = DishFactory(menu=self.menu)

    def test_get_request_return_menu_list(self):
        response = self.client.get(self.url)
        result = response.json()
        self.assertEqual(result["id"], str(self.menu.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_request_return_no_menu(self):
        dish = Dish.objects.get(id=self.dish.id)
        dish.menu = Menu.objects.get(id=self.menu_2.id)
        dish.save()
        Menu.objects.get(id=self.menu.id).delete()
        response = self.client.get(self.url)
        self.assertTrue("message" in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestMenuCreateUpdateDeleteViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/menu/"
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        self.token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_request_create_menu(self):
        dish = DishFactory()
        payload = {"options": [SimpleDishSerializer(dish).data]}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_create_menu_empty_data(self):
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_create_menu_no_options(self):
        payload = {"options": []}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_create_menu_duplicated(self):
        self.menu = MenuFactory(date=datetime.now())
        self.dish = DishFactory(menu=self.menu)
        payload = {"options": [SimpleDishSerializer(self.dish).data]}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_create_menu_fail(self):
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menu_without_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "a")
        dish = DishFactory()
        payload = {"options": [SimpleDishSerializer(dish).data]}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_delete_menu(self):
        menu = MenuFactory()
        response = self.client.delete(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_request_delete_menu_already_deleted(self):
        menu = MenuFactory()
        Menu.objects.get(id=menu.id).delete()
        response = self.client.delete(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_delete_menu_wuthout_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "a")
        menu = MenuFactory()
        response = self.client.delete(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_update_menu(self):
        menu = MenuFactory(date=datetime.now())
        now = datetime.now().date()
        payload = {"date": now}
        response = self.client.put(
            reverse("menu-detail", kwargs={"pk": menu.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_update_menu_empty(self):
        menu = MenuFactory(date=datetime.now())
        now = datetime.now().date()
        payload = {}
        response = self.client.put(
            reverse("menu-detail", kwargs={"pk": menu.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_update_menu_no_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "a")
        menu = MenuFactory(date=datetime.now())
        now = datetime.now().date()
        payload = {}
        response = self.client.put(
            reverse("menu-detail", kwargs={"pk": menu.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDishListUpdateCreateDeleteViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/dishes/"
        self.menu = MenuFactory()
        self.dish = DishFactory(menu=self.menu)
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_request_create_dish(self):
        payload = DishSerializer(self.dish).data
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_create_dish_no_data(self):
        payload = DishSerializer(self.dish).data
        response = self.client.post(self.url, data={}, format="json")
        self.assertTrue("error" in response.data)
        self.assertEqual(response.data["error"], "integrity_error")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_create_dish_no_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "a")
        payload = DishSerializer(self.dish).data
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_delete_dish(self):
        dish = DishFactory()
        response = self.client.delete(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_request_delete_dish_already_deleted(self):
        dish = DishFactory()
        Dish.objects.get(id=dish.id).delete()
        response = self.client.delete(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_delete_dish_no_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "a")
        dish = DishFactory()
        response = self.client.delete(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_update_dish(self):
        payload = {"name": "new_name", "partial": True}
        response = self.client.put(
            reverse("dish-detail", kwargs={"pk": self.dish.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_update_dish_empty_data(self):
        payload = {}
        response = self.client.put(
            reverse("dish-detail", kwargs={"pk": self.dish.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_update_dish_no_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "a")
        payload = {"name": "new_name", "partial": True}
        response = self.client.put(
            reverse("dish-detail", kwargs={"pk": self.dish.id}), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
