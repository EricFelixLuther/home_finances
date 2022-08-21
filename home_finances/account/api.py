from datetime import date, datetime

import django_filters
from rest_framework import viewsets, permissions, filters
from account.models import Operation
from account.serializers import OperationSerializer
from account.year_mixin import YearMixin


class OperationsViewSet(YearMixin, viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'category', 'user', 'tags']
    search_fields = ['title', 'user__first_name', 'category__name']

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
        queryset = self.filter_queryset(queryset)
        queryset = self.filter_date_from_to(queryset)
        queryset = queryset.order_by("-date", "-id")
        return queryset

    def filter_date_from_to(self, queryset):
        if date_from := self.request.GET.get('date_from'):
            queryset = queryset.filter(date__gte=datetime.strptime(date_from, "%Y-%m-%d"))
        if date_to := self.request.GET.get('date_to'):
            queryset = queryset.filter(date__lte=datetime.strptime(date_to, "%Y-%m-%d"))
        return queryset
