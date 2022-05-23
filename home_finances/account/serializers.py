from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.models import Operation, OperationCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationCategory
        fields = ("name", )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class OperationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()

    class Meta:
        model = Operation
        fields = ('title', 'date', 'amount', 'category', 'user')
