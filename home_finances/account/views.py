from datetime import date

import pandas
from bokeh.embed import components
from bokeh.plotting import figure
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views import View

from account.models import Operation
from account.year_mixin import YearMixin


class MainView(LoginRequiredMixin, YearMixin, View):
    template_name = 'main.html'

    def get(self, request):
        formset = modelformset_factory(Operation, fields="__all__")
        return render(request, self.template_name,
                      context={
                          "formset": formset(
                              queryset=Operation.objects.none(),
                              initial=[{"user": request.user}]
                          ),
                          "year": self._get_year(request),
                          "all_years": self._get_all_years()
                      })

    def post(self, request):
        formset = modelformset_factory(
            Operation,
            fields="__all__"
        )(
            request.POST,
            queryset=Operation.objects.none()
        )
        if formset.is_valid():
            formset.save()
            formset = modelformset_factory(
                Operation,
                fields="__all__"
            )(queryset=Operation.objects.none())
        return render(request, self.template_name,
                      context={"formset": formset,
                               "year": self._get_year(request),
                               "all_years": self._get_all_years()})


class LineView(LoginRequiredMixin, YearMixin, View):
    template_name = 'line.html'

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
        ).values()
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
        p = figure(width=900, height=1000, x_axis_type='datetime')

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
        return render(request, self.template_name, {"script": script, "div": div})
