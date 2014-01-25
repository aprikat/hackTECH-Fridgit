from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=200, db_column='full_name')
    email = models.CharField(max_length=200, db_column='email')
    password = models.CharField(max_length=200, db_column='user_password')


