from django import forms
from .models import Measurements

class MeasurementsForm(forms.ModelForm):
    class Meta:
        model = Measurements
        fields = ('destination',)