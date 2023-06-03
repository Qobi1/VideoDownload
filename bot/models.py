from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.BigIntegerField()
    state = models.IntegerField(default=0)
    request = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)