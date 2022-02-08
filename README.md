# Cornershop Test

Cornershop Test. Check out the project's [documentation](http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com:8001/).

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b9555e7e412740e39c1a?action=collection%2Fimport)

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

- You need to create a Slack App in order to send eveyone you want menu's notifications
## Create a Slack app

- To get started, create a new Slack App on [api.slack.com](https://api.slack.com/apps?new_granular_bot_app=1).
  1. Type in your app name.
  2. Select the workspace you'd like to build your app on. We recommend using a workspace where you won't disrupt real work getting done — [you can create one for free](https://slack.com/get-started#create).
     <img width="570" alt="Create-A-Slack-App" src="https://user-images.githubusercontent.com/3329665/56550657-13224680-653b-11e9-8f91-15c17e6977b7.png">

### Give your app permissions

[Scopes](https://api.slack.com/scopes) give your app permission to do things (for example, post messages) in your development workspace.

- Navigate to **OAuth & Permissions** on the sidebar to add scopes to your app

<img width="191" alt="OAuth and Permissions" src="https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/assets/oauth-permissions.png?raw=true">

- Scroll down to the **Bot Token Scopes** section and click **Add an OAuth Scope**.

For now, we'll only use one scope.

- Add the [`chat:write` scope](https://api.slack.com/scopes/chat:write) to grant your app the permission to post messages in channels it's a member of.
- Add the [`im:write` scope](https://api.slack.com/scopes/im:write) to grant your app the permission to post messages in DMs.

🎉 You should briefly see a success banner.

_If you want to change your bot user's name, click on **App Home** in the left sidebar and modify the display name._

### Install the app in your workspace

- Scroll up to the top of the **OAuth & Permissions** pages and click the green "Install App to Workspace" button.

![Install Slack app to workspace](https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/assets/oauth-installation.png?raw=true)

Next you'll need to authorize the app for the Bot User permissions.

- Click the "Allow" button.

![Authorize Slack app installation](https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/assets/authorize-install.png?raw=true)

🏁 Finally copy and save your bot token. You'll need this to communicate with Slack's Platform.
![Copy bot token](https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/assets/bot-token.png?raw=true)

---
Then you can send the url to people you want to send menus notification or you can can join a previously created workspace made for this test and the slack token preveiusly created:

- [join to slack workspace](https://join.slack.com/t/corner-testespacio/shared_invite/zt-tfxesdh1-RvHNTAVEEjsUDmXNxD4PpA) ```https://join.slack.com/t/corner-testespacio/shared_invite/zt-tfxesdh1-RvHNTAVEEjsUDmXNxD4PpA```
- ``SLACK_API_KEY=xoxp-2307232680805-2303506300838-2315637221683-c1b45610af5b4b842fa3449f5919c835```

# Initialize the project

Copy the .env.sample file to a new file called .env.

```bash
cp .env.sample .env
```
The slack bot token prevously saved, you'll need to set on your new .env, the variable is called ```SLACK_API_KEY```

update the .env entries to real values:

```bash
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
SECRET_KEY=AUniqueSecretKey
ALLOWED_HOSTS=*
SLACK_API_KEY=xxx-xxxxxxx
```

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the system as nora:

```bash
docker-compose run --rm web ./app/manage.py createsuperuser
```

## Notes

- Menus Notifications are sent at 8 AM CLT, but theres a service you can call to invoke menu's notification ```/send_menu_reminder/```
- Orders are automatically picked up from Slack at 11 a.m. CLT as well as stopped being taken at the same time, but as the reminder notification every time you call ```/api/v1/orders/``` service, the orders will be taken too, except for the ones that were not in time (11 A.M CLT)

# Documentation (running locally) 

- API Documentation  ```http://localhost:8000/api/doc/```

