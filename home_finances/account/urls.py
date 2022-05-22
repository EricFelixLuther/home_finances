from django.urls import path

from account.api import OperationsViewSet


urlpatterns = [
    path('<op_id>', OperationsViewSet.as_view(actions={'get': 'retrieve', 'put': 'update'}), name="get_op_by_id"),
    path('', OperationsViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name="get_operations"),
]
