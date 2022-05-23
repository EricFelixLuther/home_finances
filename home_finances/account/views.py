from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views import View

from account.models import Operation


class MainView(LoginRequiredMixin, View):
    template_name = 'main.html'

    def get(self, request):
        formset = modelformset_factory(Operation, fields="__all__")
        return render(request, self.template_name,
                      context={"formset": formset(queryset=Operation.objects.none())})

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
                      context={"formset": formset})
