from datetime import datetime
from django.utils import timezone
from django.db import models
from .utils import _generate_ID_, _getToken_


class User(models.Model):
    userID = models.CharField(max_length=5, default=_generate_ID_)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    referral_code = models.CharField(max_length=4, null=True)
    referral_score = models.IntegerField(default=0)
    registered_time = models.CharField(max_length=20, default=datetime.now().timestamp())
    # datetime.fromtimestamp(timestamp)

    def __str__(self):
        return f"user_{self.name}"


    def get_token(self, user):
        login = LoginHistory(user=user)
        login.save()
        return {
            "token": login.token,
            "userID": self.userID,
            "status": "Successfully generated data"
        }


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=15, default=_getToken_)
    last_login_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}_{self.token}"
