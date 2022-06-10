from django.urls import path

from charts.api import LineChartApiView, ExpensesBarChartApiView

urlpatterns = [
    path('line', LineChartApiView.as_view(), name="line_chart"),
    path('expenses', ExpensesBarChartApiView.as_view(), name="expenses_chart"),
]