from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Korisnik, Predmeti, Upisi
# Create your views here.


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role.role == 'STUDENT':
            return '/upisni-list/'
        else:
            return '/dashboard/'


class UpisniListView(LoginRequiredMixin, ListView):
    template_name = 'upisniList.html'
    context_object_name = 'predmeti_list'

    def get_queryset(self):
        return Predmeti.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        enrollments = Upisi.objects.filter(studentId=user)
        enrolled_predmeti = enrollments.values_list('predmetId', flat=True)
        context['enrolled_predmeti'] = enrolled_predmeti
        return context