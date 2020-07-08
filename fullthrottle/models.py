from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    real_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class ActivityPeriod(models.Model):
    start_time = models.DateTimeField('start_time')
    end_time = models.DateTimeField('end_time')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
