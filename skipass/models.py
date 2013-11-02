from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    card_number = models.IntegerField(unique=True)
    balance = models.IntegerField(default=0)
    days_left = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username