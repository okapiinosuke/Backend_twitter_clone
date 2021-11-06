from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Account(User):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.username
