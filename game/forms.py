from django import forms
from .models import *

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']

class RoundForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['unmultiplied_round_score',
                  'multiplicator']
        labels = {'unmultiplied_round_score': 'raw',
                  'multiplicator': 'x'}