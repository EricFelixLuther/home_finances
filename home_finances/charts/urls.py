from django.urls import path

from charts.api import LineChartApiView, ExpensesBarChartApiView, ExpensesPieChartYearSummary, \
    ExpensesCategoriesPieChartYearSummary

urlpatterns = [
    path('line', LineChartApiView.as_view(), name="line_chart"),
    path('expenses', ExpensesBarChartApiView.as_view(), name="expenses_chart"),
    path('pie', ExpensesPieChartYearSummary.as_view(), name="expenses_pie"),
    path('categories_pie', ExpensesCategoriesPieChartYearSummary.as_view(), name="categories_pie"),
]