from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.views import View
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

        predmeti_list = context['predmeti_list']
        if user.status == 'red':
            for predmet in predmeti_list:
                if predmet.pk in enrolled_predmeti and predmet:
                    predmet.is_enrolled = True
                    predmet.semester = predmet.sem_red
                else:
                    predmet.is_enrolled = False
                    predmet.semester = predmet.sem_izv

        if user.status == 'red':
                listSortedPredmeti = sorted(predmeti_list, key=lambda x: x.semester)
                
               
            
        semesters = set(predmet.semester for predmet in predmeti_list)
        lsSortedSemesters = sorted(semesters)

        context['semesters'] = lsSortedSemesters
        context['predmeti_list'] = listSortedPredmeti
        return context



    
        
    

class EnrollSubjectView(View):
    def post(self, request, pk):
        predmet = Predmeti.objects.get(pk=pk)
        Upisi.objects.create(studentId=request.user, predmetId=predmet, status='upisan')
        return redirect('upisniList')

class DerollSubjectView(View):
    def post(self, request, pk):
        Upisi.objects.filter(studentId=request.user, predmetId=pk).delete()
        return redirect('upisniList')
    


