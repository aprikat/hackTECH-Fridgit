from django.db import models
from django.contrib.auth.models import User as U
'''
class User(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200, db_column='full_name')
    email = models.CharField(max_length=200, db_column='email')
    password = models.CharField(max_length=200, db_column='user_password')
'''
class Food(models.Model):
    id = models.Integerid = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200, db_column='name')
    quantity = models.Integerid = models.IntegerField(default=0)
    user = models.ForeignKey(U)
