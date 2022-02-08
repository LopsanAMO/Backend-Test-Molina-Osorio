import pytz
from datetime import datetime, timezone
from slack import WebClient
from slack.errors import SlackApiError
from corner_test.apps.employees.models import Employee
from corner_test.apps.menus.models import Order, Dish
from corner_test.apps.utils.exceptions import (
    SlackUserListException,
    SlackChannelListException,
    EmployeeDoesNotExistException,
    SlaskUserInfoException,
    SlackErrorException,
    SlackGetMessageException,
    SlackGetChannelException,
    SlackSendMessageException,
)


class SlackService:
    def __init__(self, SLACK_API_KEY):
        self.client = WebClient(SLACK_API_KEY)

    def save_employees(self, users_array=[]):
        for user in users_array:
            try:
                if user["is_bot"] == False and user["name"] != "Nora":
                    user_id = user["id"]
                    username = user["profile"]["real_name"]
                    Employee.objects.get_or_create(slack_user_id=user_id, name=username)
            except KeyError as e:
                raise SlackUserListException(
                    "slack data is different than the expected" + str(e)
                )

    def save_channel(self, conversations=[], user_id=None):
        try:
            for c in conversations:
                if c["user"] == user_id:
                    employee = Employee.objects.get(slack_user_id=user_id)
                    employee.channel_id = c["id"]
                    employee.save()
                    return c["id"]
            return None
        except KeyError as e:
            raise SlackChannelListException(
                "slack data is different than the expected" + str(e)
            )
        except Employee.DoesNotExist as e:
            raise EmployeeDoesNotExistException(str(e))
        except Exception as e:
            raise SlackUserListException(str(e))

    def get_users_info(self):
        try:
            result = self.client.users_list()
            self.save_employees(result["members"])
            return [
                user["id"]
                for user in result["members"]
                if user["is_bot"] == False and user["name"] != "Nora"
            ]
        except SlackApiError as e:
            raise SlackErrorException(e.response["error"])
        except SlackUserListException as e:
            raise SlackUserListException(str(e))
        except KeyError as e:
            raise SlaskUserInfoException(
                "slack data is different than the expected" + str(e)
            )
        except Exception as e:
            raise SlaskUserInfoException(str(e))

    def get_channel(self, user_id):
        try:
            result = self.client.conversations_list(params={"types": "im"})
            channel = self.save_channel(result["channels"], user_id)
            return channel
        except SlackApiError as e:
            raise SlackErrorException(e.response["error"])
        except Exception as e:
            raise SlackGetChannelException(str(e))

    def send_messages(self, users, menu_data):
        data = [
            {"type": "section", "text": {"type": "plain_text", "text": "Hello!"}},
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "I share with you today's menu :)",
                },
            },
        ]
        for menu in menu_data["options"]:
            data.append(
                {"type": "section", "text": {"type": "plain_text", "text": menu}}
            )
        data.append(
            {
                "type": "section",
                "text": {"type": "plain_text", "text": "Have a nice day!"},
            }
        )
        try:
            data.append(
                {
                    "type": "actions",
                    "block_id": "actionblock789",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Abrir Menu"},
                            "url": "http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com/api/v1/menu/{}/".format(
                                menu_data["id"]
                            ),
                        }
                    ],
                }
            )
        except Exception:
            pass
        try:
            for user in users:
                result = self.client.chat_postMessage(
                    channel=user, as_user=True, blocks=data
                )
                employee = Employee.objects.get(slack_user_id=user)
                if not employee.channel_id:
                    employee.channel_id = result["channel"]
                    employee.save()
        except SlackApiError as e:
            raise SlackErrorException(e.response["error"])
        except Exception as e:
            raise SlackSendMessageException(str(e))

    def get_messages(self):
        for user in (
            Employee.objects.all().exclude(name="Slackbot").exclude(name="Nora")
        ):
            if not user.channel_id:
                channel = self.get_channel(user.slack_user_id)
            else:
                channel = user.channel_id
            if not channel:
                return
            now = datetime.now()
            init_daily_timestamp = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=8,
                minute=0,
                tzinfo=pytz.timezone("America/Santiago"),
            ).timestamp()
            end_limit_timestamp = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=11,
                minute=0,
                tzinfo=pytz.timezone("America/Santiago"),
            ).timestamp()
            try:
                results = self.client.conversations_history(
                    channel=channel,
                    oldest=init_daily_timestamp,
                    latest=end_limit_timestamp,
                )
                messages = [i["text"] for i in results["messages"] if i]
                option = None
                for message in messages:
                    if "option" in message.lower():
                        option = message
                if option:
                    option = int(option.replace("option", "").replace(" ", ""))
                    dish = Dish.objects.get(id=option)
                    specifications = ", ".join(messages)
                    order, created = Order.objects.get_or_create(
                        dish=dish, employee=user
                    )
                    order.specifications = specifications
                    order.save()
            except SlackApiError as e:
                raise SlackErrorException(e.response["error"])
            except Exception as e:
                raise SlackGetMessageException(str(e))
