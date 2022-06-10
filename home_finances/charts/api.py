from datetime import date

import pandas
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from django.db.models import Count, Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Operation
from account.year_mixin import YearMixin


class LineChartApiView(YearMixin, APIView):
    template_name = 'line.html'
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        year = self._get_year(request)
        operations = Operation.objects.filter(
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


class ExpensesBarChartApiView(YearMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get(self, request):
        year = self._get_year(request)
        operations = Operation.objects.filter(
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

# Additional charts:
# - expenses / gains per month - slupki
# - expenses / gains per person - circle
# - expenses per category - circle
