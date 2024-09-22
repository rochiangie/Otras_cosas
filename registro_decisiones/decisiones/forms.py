# decisiones/forms.py
from django import forms
from .models import RegistroDecision, RegistroMenstrual

class DecisionForm(forms.ModelForm):
    class Meta:
        model = RegistroDecision
        fields = ['fecha', 'decision', 'nota', 'estado_animo', 'premenstrual', 'evento_inusual']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'decision': forms.Textarea(attrs={'placeholder': 'Escribe tu decisión aquí...'}),
            'nota': forms.Textarea(attrs={'placeholder': 'Notas adicionales...'}),
            'estado_animo': forms.Select(choices=[
                ('feliz', 'Feliz'),
                ('triste', 'Triste'),
                ('ansioso', 'Ansioso'),
                ('neutral', 'Neutral'),
            ]),
        }

class MenstrualForm(forms.ModelForm):
    class Meta:
        model = RegistroMenstrual
        fields = ['fecha', 'sintomas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'sintomas': forms.Textarea(attrs={'placeholder': 'Describe los síntomas...'}),
        }
