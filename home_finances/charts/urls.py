from django.urls import path

from charts.api import LineChartApiView

urlpatterns = [
    path('line', LineChartApiView.as_view(), name="line_chart"),
]