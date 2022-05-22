from rest_framework import serializers

from account.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('title', 'date', 'amount', 'category', 'user')
