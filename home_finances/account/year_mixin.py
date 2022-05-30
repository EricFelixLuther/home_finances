from datetime import date

from account.models import Operation


class YearMixin:
    def _get_year(self, request):
        return int(request.GET.get("year", date.today().year))

    def _get_all_years(self):
        all_operations = Operation.objects.all().values_list("date", flat=True).distinct()
        return set([each.year for each in all_operations])
