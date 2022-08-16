from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory, modelform_factory
from django.shortcuts import render
from django.views import View

from account.models import Operation
from account.year_mixin import YearMixin


class MainView(LoginRequiredMixin, YearMixin, View):
    template_name = 'main.html'

    def get(self, request):
        formset = self._get_formset(None, request.user)
        return render(request, self.template_name,
                      context=self._get_context(request, formset))

    def post(self, request):
        formset = self._get_formset(request.POST, request.user)
        if formset.is_valid():
            formset.save()
            formset = self._get_formset(None, request.user)
        return render(request,
                      self.template_name,
                      context=self._get_context(request, formset))

    def _get_formset(self, request_post, request_user):
        formset = modelformset_factory(Operation, fields="__all__")
        return formset(
            request_post or None,
            queryset=Operation.objects.none(),
            initial=[{"user": request_user}]
        )

    def _get_context(self, request, formset):
        return {"formset": formset,
                "form": modelform_factory(Operation, fields="__all__"),
                "year": self._get_year(request),
                "all_years": self._get_all_years()}
