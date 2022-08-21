from datetime import date
from decimal import Decimal
from math import pi

import pandas
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange, LabelSet
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, cumsum
from django.db.models import Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Operation
from account.year_mixin import YearMixin


class OperationsChartApiMixin(YearMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_operations_from_year(self, request):
        year = self._get_year(request)
        return Operation.objects.filter(
            date__year=year
        ).select_related(
            "category", "user"
        )


class LineChartApiView(OperationsChartApiMixin, APIView):
    template_name = 'line.html'
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        operations = self.get_operations_from_year(
            request
        ).order_by("date").values()
        df = pandas.DataFrame(list(operations))
        df["kumulatywnie"] = df['amount'].cumsum()  # kumulatywna kolumna oszczędności
        # krzysiek = df[df['kto'] == 'Krzysiek']  # Wydatki Krzyśka
        # agata = df[df['kto'] == 'Agata']  # Wydatki Agaty

        # Dane
        today = date.today()
        year_start = date(today.year, 1, 1)
        days_since_start = (today - year_start).days
        cel = 50000
        # saved = df['kasa'].sum()
        should_be_saved_by_today = (cel / 365) * days_since_start

        # Utwórz wykres
        p = figure(width=1600, height=850, x_axis_type='datetime')

        # Dodaj wykresy wydatków
        p.line(df['date'], df['kumulatywnie'], color="Black", alpha=1.0, line_color="Black",
               legend_label="Przychody/rozchody całkowite")
        # p.circle(df['data'], df['kumulatywnie'], color="Black", alpha = 1.0, line_color="Black", legend_label="Przychody/rozchody dokładnie")
        # p.circle(krzysiek['data'], krzysiek['kumulatywnie'], color="Blue", alpha = 1.0, line_color="Blue", legend_label="Przychody/rozchody Krzyśka")
        # p.circle(agata['data'], agata['kumulatywnie'], color="Red", alpha = 1.0, line_color="Red", legend_label="Przychody/rozchody Agaty")

        # Linie orientacyjne
        p.line(df['date'], 0, color="Red", alpha=1.0, line_color="Red", legend_label="Granica zero")
        p.line(df['date'], cel, color="Green", alpha=1.0, line_color="Green", legend_label="Cel na rok 2021")
        p.line(df['date'], should_be_saved_by_today, color="Yellow", alpha=1.0, line_color="Yellow",
               legend_label="Powinno być na dziś")

        # Legenda
        p.legend.location = 'top_left'
        p.legend.title = 'Wykres oszczędności 2021'
        p.legend.title_text_font = 'Arial'
        p.legend.title_text_font_size = '20pt'

        script, div = components(p)
        return Response({"script": script, "div": div}, template_name=self.template_name)


class ExpensesBarChartApiView(OperationsChartApiMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        operations = self.get_operations_from_year(request)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        data = {'months': months,
                'expense': [0 for i in range(len(months))],
                'gain': [0 for i in range(len(months))]}
        palette = ["#11e812", "#e84d60"]
        for each in operations:
            if each.amount > 0:
                data['gain'][each.date.month - 1] += each.amount
            else:
                data['expense'][each.date.month - 1] += (each.amount * -1)
        x = [(month, amount) for month in months for amount in ('gain', 'expense')]
        values = sum(zip(data['gain'], data['expense']), ())
        source = ColumnDataSource(data=dict(x=x, values=values))
        p = figure(width=1600, height=850, x_range=FactorRange(*x), title="Expenses and gains per month")
        p.vbar(x="x", top="values", width=0.9, source=source, fill_color=factor_cmap(
            'x', palette=palette, factors=['gain', 'expense'], start=1, end=2
        ))
        script, div = components(p)
        return Response({"script": script, "div": div})


class ExpensesBarChartWithUsersApiView(OperationsChartApiMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        """
        TODO: This is WIP.
        This view renders a stacked vbar that calculates per month in a selected year, per gain/expense how much each
        person gained/spent. On x should be a combination of month/gain-expense, and on stacks are persons.
        """
        operations = self.get_operations_from_year(request)
        first_x = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        second_x = ['gain', 'expense']
        factors = [(f_x, s_x) for f_x in first_x for s_x in second_x]
        stacks = list(operations.values_list("user__first_name", flat=True).distinct())
        iterable = [first_x, second_x]
        index = pandas.MultiIndex.from_product(iterable, names=["Months", "Operation type"])
        # creates double axis
        factors = [(f_x, s_x) for f_x in first_x for s_x in second_x]
        data_dict = {
            "x": factors
        }
        for each in operations:
            pass
        source = ColumnDataSource(data=data_dict)
        data = {'months': first_x,
                'expense': [0 for i in range(len(first_x))],
                'gain': [0 for i in range(len(first_x))]}
        palette = ["#11e812", "#e84d60"]
        for each in operations:
            if each.amount > 0:
                data['gain'][each.date.month - 1] += each.amount
            else:
                data['expense'][each.date.month - 1] += (each.amount * -1)
        x = [(month, amount) for month in first_x for amount in ('gain', 'expense')]
        values = sum(zip(data['gain'], data['expense']), ())
        source = ColumnDataSource(data=dict(x=x, values=values))
        p = figure(width=1600, height=850, x_range=FactorRange(*x), title="Expenses and gains per month")
        p.vbar(x="x", top="values", width=0.9, source=source, fill_color=factor_cmap(
            'x', palette=palette, factors=['gain', 'expense'], start=1, end=2
        ))
        script, div = components(p)
        return Response({"script": script, "div": div})


class ExpensesPieChartYearSummary(OperationsChartApiMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        operations = self.get_operations_from_year(request).filter(amount__lt=0)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        expenses_per_months = {}
        for i, month in enumerate(months):
            expenses_per_current_month = operations.filter(
                    date__month=i + 1
                ).aggregate(
                    exp_per_month=Sum("amount")
                )['exp_per_month']
            if expenses_per_current_month:
                expenses_per_months[month] = round(expenses_per_current_month, 0)
        data = pandas.Series(expenses_per_months).reset_index(name='value').rename(columns={'index': 'month'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * Decimal(pi)
        data['color'] = Category20c[len(expenses_per_months)]

        p = figure(height=800, width=1000, title="Expenses per month", toolbar_location=None,
                   tools="hover", tooltips="@month: @value", x_range=(-0.5, 1.0))
        p.wedge(x=0, y=1, radius=0.5,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='month', source=data)
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        script, div = components(p)
        return Response({"script": script, "div": div})


class ExpensesCategoriesPieChartYearSummary(OperationsChartApiMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        operations = self.get_operations_from_year(request).filter(amount__lt=0)
        expenses_per_cat = {
            category: round(operations.filter(category__name=category).aggregate(exp_per_cat=Sum("amount"))['exp_per_cat'], 0)
            for category in operations.values_list("category__name", flat=True)
        }
        data = pandas.Series(expenses_per_cat).reset_index(name='value').rename(columns={'index': 'category'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * Decimal(pi)
        data['color'] = Category20c[len(expenses_per_cat)]

        p = figure(height=800, width=1000, title="Expenses per category", toolbar_location=None,
                   tools="hover", tooltips="@category: @value", x_range=(-0.5, 1.0))
        p.wedge(x=0, y=1, radius=0.5,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='category', source=data)
        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        script, div = components(p)
        return Response({"script": script, "div": div})


# TODO Additional charts:
# - expenses / gains per person - circle
# - expenses per tag - single tag bar per month
# - expenses per category - stacked bars per month with differentation per person
