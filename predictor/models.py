from django.db import models

class User(models.Model):

    user_name = models.CharField(max_length=32, unique=True, null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)
    avatar = models.CharField(max_length=258, null=True, blank=True)
    register_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user_name

class UserToken(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.token

class Stock(models.Model):
    user = models.ManyToManyField('User')
    stock_id = models.CharField(max_length=8)

    def __str__(self):
        return self.stock_id







