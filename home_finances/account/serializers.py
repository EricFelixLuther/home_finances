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
    category = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = ('title', 'date', 'amount', 'category', 'user')

    def get_user(self, obj):
        return obj.user.first_name

    def get_category(self, obj):
        if obj.category:
            return obj.category.name
        else:
            return ''
