from datetime import date

from rest_framework import viewsets, permissions
from rest_framework.views import APIView

from account.models import Operation
from account.serializers import OperationSerializer
from account.year_mixin import YearMixin


class OperationsViewSet(YearMixin, viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all().order_by("-date", "title")
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self._get_year(self.request)
        return super().get_queryset().filter(
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
