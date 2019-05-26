from django import forms

from .models import TestingFormModel


class TestingForm(forms.ModelForm):

    class Meta:
        model = TestingFormModel
        fields = '__all__'
