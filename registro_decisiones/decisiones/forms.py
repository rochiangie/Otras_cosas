from django import forms
from .models import RegistroDecision

class DecisionForm(forms.ModelForm):
    class Meta:
        model = RegistroDecision
        fields = ['fecha', 'decision', 'nota', 'estado_animo', 'premenstrual', 'evento_inusual']
