from django.forms import ModelForm,Textarea
from django import forms

from main.models import Tutorial

class TutorialForm(ModelForm):
  class Meta:
    model = Tutorial
    fields = ['desc']
    widgets = {
      'summary': forms.Textarea(attrs={'rows':1, 'cols':1}),
    }