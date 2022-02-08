import mock
from django.test import TestCase
from corner_test.apps.employees.models import Employee
from corner_test.apps.menus.models import Dish, Order, Menu
from corner_test.apps.employees.tests.factories import EmployeeFactory
from corner_test.apps.menus.tests.factories import MenuFactory, DishFactory
from corner_test.apps.menus.serializers import MenuSerializer
from corner_test.apps.utils.slack import SlackService
from corner_test.apps.utils.exceptions import (
    SlackUserListException,
    SlackChannelListException,
    EmployeeDoesNotExistException,
    SlaskUserInfoException,
    SlackErrorException,
    SlackSendMessageException,
)


def mocked_slack_user_list(**kargs):
    return {
        "members": [
            {
                "id": "4GB601",
                "is_bot": False,
                "name": "test",
                "profile": {"real_name": "slack_test"},
            }
        ]
    }


def mocked_slack_error_user_list(**kargs):
    return {"members": [{"id": "4GB601", "profile": {"real_name": "slack_test"}}]}


def mocked_slack_channel(**kargs):
    return {
        "channels": [
            {
                "id": "D029TTS7B4G",
                "created": 1627259796,
                "is_archived": False,
                "is_im": True,
                "is_org_shared": False,
                "user": "FSAF2133",
                "is_user_deleted": False,
                "priority": 0,
            }
        ]
    }


def mocked_slack_messages(**kwargs):
    return {
        "messages": [
            {
                "bot_id": "B029Z3ML08Y",
                "type": "message",
                "text": "option 1",
                "user": "FSAF2133",
                "ts": "1627391934.013700",
                "team": "T02916UL0PP",
            }
        ]
    }


def mocked_slack_post_message(**kwargs):
    return {
        "ok": True,
        "channel": "FDSFD3434S43",
        "ts": "1627473015.000100",
        "message": {
            "bot_id": "B029Z3ML08Y",
            "type": "message",
            "text": "test",
            "user": "U028XEW8UQN",
            "ts": "1627473015.000100",
            "team": "T02916UL0PP",
            "bot_profile": {
                "id": "B029Z3ML08Y",
                "deleted": False,
                "name": "Nora",
                "updated": 1627370441,
                "app_id": "A0291CYFTLM",
                "team_id": "T02916UL0PP",
            },
        },
    }


class TestSlackService(TestCase):
    def setUp(self):
        self.service = SlackService("SSSSSS")

    def test_slack_save_employees(self):
        self.service.save_employees(mocked_slack_user_list()["members"])
        employee = Employee.objects.get(slack_user_id="4GB601")
        self.assertEqual(employee.name, "slack_test")

    def test_slack_save_employees_error(self):
        with self.assertRaises(SlackUserListException):
            self.service.save_employees(mocked_slack_error_user_list()["members"])

    def test_slack_save_channel_wrong_data(self):
        with self.assertRaises(SlackChannelListException):
            channels = mocked_slack_user_list()["members"]
            self.service.save_channel(channels)

    def test_slack_save_channel_no_user(self):
        with self.assertRaises(EmployeeDoesNotExistException):
            channels = mocked_slack_channel()["channels"]
            self.service.save_channel(channels, "FSAF2133")

    @mock.patch("slack.WebClient.users_list", side_effect=mocked_slack_user_list)
    def test_slack_service_get_users(self, mock_slack):
        self.service.get_users_info()
        employee = Employee.objects.get(slack_user_id="4GB601")
        self.assertEqual(employee.name, "slack_test")

    def test_slack_service_get_users_slack_with_invalid_auth(self):
        with self.assertRaises(SlackErrorException):
            self.service.get_users_info()
            employee = Employee.objects.get(slack_user_id="4GB601")
            self.assertEqual(employee.name, "slack_test")

    @mock.patch("slack.WebClient.users_list", side_effect=mocked_slack_channel)
    def test_slack_service_get_users_wrong_data(self, mock_slack):
        with self.assertRaises(SlaskUserInfoException):
            self.service.get_users_info()

    @mock.patch("slack.WebClient.conversations_list", side_effect=mocked_slack_channel)
    def test_slack_service_get_channel(self, mock_slack_channel):
        users = mocked_slack_user_list()
        EmployeeFactory(slack_user_id="FSAF2133")
        users["members"][0]["id"] = "FSAF2133"
        self.service.get_channel("FSAF2133")
        employee = Employee.objects.get(slack_user_id="FSAF2133")
        self.assertEqual(employee.channel_id, "D029TTS7B4G")

    def test_slack_service_get_channel_with_invalid_auth(self):
        with self.assertRaises(SlackErrorException):
            users = mocked_slack_user_list()
            EmployeeFactory(slack_user_id="FSAF2133")
            users["members"][0]["id"] = "FSAF2133"
            self.service.get_channel("FSAF2133")
            employee = Employee.objects.get(slack_user_id="FSAF2133")
            self.assertEqual(employee.channel_id, "D029TTS7B4G")

    @mock.patch("slack.WebClient.conversations_list", side_effect=mocked_slack_channel)
    @mock.patch(
        "slack.WebClient.conversations_history", side_effect=mocked_slack_messages
    )
    def test_slack_get_messages(self, mock, mock2):
        Menu.objects.get_or_create(id=1)
        Dish.objects.get_or_create(id=1, menu_id=1)
        employee = EmployeeFactory(slack_user_id="FSAF2133")
        self.service.get_messages()
        self.assertTrue(Order.objects.all())

    def test_slack_get_messages_channels_not_found(self):
        with self.assertRaises(SlackErrorException):
            Menu.objects.get_or_create(id=1)
            Dish.objects.get_or_create(id=1, menu_id=1)
            employee = EmployeeFactory(slack_user_id="FSAF2133")
            self.service.get_messages()
            self.assertTrue(Order.objects.all())

    @mock.patch(
        "slack.WebClient.chat_postMessage", side_effect=mocked_slack_post_message
    )
    def test_slack_send_messages(self, mockc):
        menu = MenuFactory()
        dish = DishFactory(menu=menu)
        menu_data = MenuSerializer(menu).data
        EmployeeFactory(slack_user_id="FSAF213312", channel_id=None)
        self.service.send_messages(["FSAF213312"], menu_data)
        employee = Employee.objects.get(slack_user_id="FSAF213312")
        self.assertEqual(employee.channel_id, "FDSFD3434S43")

    def test_slack_send_messages_with_invalid_auth(self):
        with self.assertRaises(SlackErrorException):
            menu = MenuFactory()
            dish = DishFactory(menu=menu)
            menu_data = MenuSerializer(menu).data
            EmployeeFactory(slack_user_id="FSAF213312", channel_id=None)
            self.service.send_messages(["FSAF213312"], menu_data)
            employee = Employee.objects.get(slack_user_id="FSAF213312")
            self.assertEqual(employee.channel_id, "FDSFD3434S43")

    @mock.patch(
        "slack.WebClient.chat_postMessage", side_effect=mocked_slack_post_message
    )
    def test_slack_send_messages_with_invalid_auth_2_invalid_user(
        self, mock_slack_message
    ):
        with self.assertRaises(SlackSendMessageException):
            menu = MenuFactory()
            dish = DishFactory(menu=menu)
            menu_data = MenuSerializer(menu).data
            EmployeeFactory(slack_user_id="FSAF213342", channel_id=None)
            self.service.send_messages(["FSAF213312"], menu_data)
            employee = Employee.objects.get(slack_user_id="FSAF213312")
            self.assertEqual(employee.channel_id, "FDSFD3434S43")
