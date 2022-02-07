from django.db import models


class Employee(models.Model):
    slack_user_id = models.CharField(max_length=20, null=False, blank=False, unique=True)
    channel_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=40)