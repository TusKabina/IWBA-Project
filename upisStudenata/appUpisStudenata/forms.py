# forms.py

from django import forms
from .models import Predmeti, Korisnik
from django.contrib.auth.hashers import make_password

class PredmetForm(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program','ects','sem_red', 'sem_izv', 'izborni','nositelj']

class UserForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ['username', 'password', 'role','status']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
