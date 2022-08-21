from rest_framework import serializers

from account.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('pk', 'title', 'date', 'amount', 'category', 'user', 'tags')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.category:
            rep['category'] = {'id': instance.category.id,
                               'name': instance.category.name}
        else:
            rep['category'] = {'id': '',
                               'name': ''}
        rep['user'] = {'id': instance.user.id,
                       'name': f'{instance.user.first_name} {instance.user.last_name}'}
        if tags := instance.tags.all():
            rep['tags'] = [{'id': tag.id, 'name': tag.name} for tag in tags]
        else:
            rep['tags'] = []
        return rep
