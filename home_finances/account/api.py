from datetime import date

import django_filters
from rest_framework import viewsets, permissions
from account.models import Operation
from account.serializers import OperationSerializer
from account.year_mixin import YearMixin


class OperationsViewSet(YearMixin, viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        year = self._get_year(self.request)
        queryset = Operation.objects.filter(
            date__gte=date(
                year=year,
                month=1,
                day=1
            )
        ).filter(
            date__lte=date(
                year=year,
                month=12,
                day=31
            )
        )
        queryset = self.filter_queryset(queryset).order_by("-date", "id")
        return queryset
