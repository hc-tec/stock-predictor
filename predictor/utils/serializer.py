
import json
from datetime import datetime
from django.core.serializers import serialize
from rest_framework import serializers
from .. import models

class UserInfoSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()

    def get_token(self, row):
        return models.UserToken.objects. \
            filter(user=row).first().__dict__['token']

    class Meta:
        model = models.User
        fields = ['id', 'user_name', 'avatar', 'token', 'register_time']

class StockSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Stock
        fields = ['stock_id']
