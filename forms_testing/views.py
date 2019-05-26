from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import TestingForm as tf


class TestingForm(CreateView):

    form_class = tf
    redirect_field_name = "testing_form"
    success_url = reverse_lazy("testing_form")
    template_name = "TestingForm.html"

    def form_valid(self, form):
        return super(TestingForm, self).form_valid(form)
