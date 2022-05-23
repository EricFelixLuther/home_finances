from rest_framework import viewsets, permissions

from account.models import Operation
from account.serializers import OperationSerializer


class OperationsViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all().order_by("-date", "title")
    permission_classes = [permissions.IsAuthenticated]
