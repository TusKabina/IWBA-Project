from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Korisnik, Predmeti, Upisi, Role
from .forms import PredmetForm, UserForm
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
# Create your views here.


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        studentId = user.id
        if user.role.role == 'STUDENT':
            return reverse_lazy('upisniList', kwargs={'student_id': studentId})
        elif user.role.role == "ADMIN":
            return reverse_lazy('listPredmeti')
        elif user.role.role == "PROFESOR":
            return reverse_lazy('predmetiProfesora')

class UpisniListView(LoginRequiredMixin, ListView):
    template_name = 'upisniList.html'
    context_object_name = 'predmeti_list'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN' and request.user.role.role != 'STUDENT':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Predmeti.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('student_id') 
        user = self.request.user
        student = get_object_or_404(Korisnik, pk=student_id)
        if not student_id:
            student = user
            
        
        enrollments = Upisi.objects.filter(studentId=student)
        enrolled_predmeti = enrollments.values_list('predmetId', flat=True)
        
        predmeti_list = context['predmeti_list']
        

        for predmet in predmeti_list:
            if predmet.pk in enrolled_predmeti and predmet:
                predmet.is_enrolled = True
                predmet.semester = predmet.sem_red if user.status == 'red' else predmet.sem_izv
                try:
                    enrolled_predmet = enrollments.filter(predmetId=predmet.pk).first()
                    predmet.status = enrolled_predmet.status
                except Upisi.DoesNotExist:
                    predmet.status = 'NE RADI' 
            else:
                predmet.is_enrolled = False
                predmet.semester = predmet.sem_red if user.status == 'red' else predmet.sem_izv

        
        listSortedPredmeti = sorted(predmeti_list, key=lambda x: x.semester)
        semesters = set(predmet.semester for predmet in predmeti_list)
        lsSortedSemesters = sorted(semesters)
        osvojeniECTS = Predmeti.objects.filter(predmet__studentId = student,predmet__status='polozen').aggregate(osvojeniECTS = Sum("ects"))
        sveukupniECTS = Predmeti.objects.filter(predmet__studentId=student,predmet__status = 'upisan').aggregate(sveukupniECTS = Sum("ects"))
        context['semesters'] = lsSortedSemesters
        context['predmeti_list'] = listSortedPredmeti
        context['student'] = student
        context['osvojeniECTS'] = osvojeniECTS['osvojeniECTS']
        context['sveukupniECTS'] = sveukupniECTS["sveukupniECTS"]
        return context



class PredmetiListView(LoginRequiredMixin, ListView):
    model = Predmeti
    template_name = 'listPredmeti.html'
    context_object_name = 'predmeti_list'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    

# class IspitPredmetiListView(LoginRequiredMixin, ListView):
#     model = Predmeti
#     template_name = 'ispitListPredmeti.html'
#     context_object_name = 'predmeti_list'
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('login')
        
#         if request.user.role.role != 'ADMIN' and request.user.role.role != 'PROFESOR':
#             return HttpResponseForbidden("Access Denied")
#         return super().dispatch(request, *args, **kwargs)
    
#     def get_queryset(self):
#         return Predmeti.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         predmeti_list = context['predmeti_list']
            
#         for predmet in predmeti_list:
#             polozeniStudenti = Upisi.objects.filter(predmetId__name = predmet.name,status = "polozen").count()
#             sem_redPolozeni = Upisi.objects.filter(predmetId__name = predmet.name,status = "polozen",studentId__status = 'red').count()
#             sem_izvPolozeni = Upisi.objects.filter(predmetId__name = predmet.name,status = "polozen",studentId__status = 'izv').count()
#             predmet.polozeniStudenti = polozeniStudenti
#             predmet.sem_redPolozeni = sem_redPolozeni
#             predmet.sem_izvPolozeni = sem_izvPolozeni

#         context['predmeti_list'] = predmeti_list

#         return context
    
# class IspitDetaljiPolozenihStudenata(LoginRequiredMixin, View):
#      def get(self, request, predmet_id):
#         predmet = get_object_or_404(Predmeti, pk=predmet_id)
#         polozeniStudenti = Korisnik.objects.filter(student__predmetId=predmet,student__status = 'polozen').distinct()
        
#         context = {
#             'predmet': predmet,
#             'studenti_list': polozeniStudenti
#         }
#         return render(request, 'ispitPolozeniStudenti.html', context)

# class ispitDetaljiPredmeta(LoginRequiredMixin, View):
#     def get(self, request, predmet_id):
#         predmet = get_object_or_404(Predmeti, pk=predmet_id)
#         context = {
#             'predmet': predmet,
#         }
#         return render(request, 'ispitPolozeniStudenti.html', context)








class IspitListaPredmeta(LoginRequiredMixin, ListView):
    model = Predmeti
    template_name = 'ispitListaPredmeta.html'
    context_object_name = 'predmeti_list'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        return Predmeti.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        predmeti_list = context['predmeti_list']

        for predmet in predmeti_list:
            sveukupnoPolozeni = Upisi.objects.filter(predmetId = predmet, status='polozen').count()
            polozeniRed = Upisi.objects.filter(predmetId = predmet, studentId__status = 'red', status ='polozen').count()
            izv = Upisi.objects.filter(predmetId = predmet, studentId__status = 'izv', status = 'polozen').count()
            predmet.polozeno = sveukupnoPolozeni
            predmet.red = polozeniRed

        context['predmeti_list'] = predmeti_list
        return context




















class PredmetiUpdateView(LoginRequiredMixin, UpdateView):
    model = Predmeti
    fields = ['name', 'kod', 'sem_red', 'sem_izv', 'ects', 'nositelj','program']
    template_name = 'predmetiEdit.html'
    success_url = '/list-predmeti/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN' and request.user.role.role != 'PROFESOR':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        profesor_role = Role.objects.get(role=Role.PROFESOR)
        form.fields['nositelj'].queryset = form.fields['nositelj'].queryset.filter(role=profesor_role)
        if self.request.user.role.role == 'PROFESOR':
            del form.fields["name"]
            del form.fields["kod"]
            del form.fields["sem_red"]
            del form.fields["sem_izv"]
            del form.fields["ects"]
            del form.fields["nositelj"]

        return form

class PredmetiCreateView(LoginRequiredMixin, View):
     login_url = '/login/'
     redirect_field_name = 'redirect_to'
     def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        form = PredmetForm()
        return render(request, 'createPredmet.html', {'form': form})

     def post(self, request):
        form = PredmetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listPredmeti')
        return render(request, 'createPredmet.html', {'form': form})

class StudentiListView(LoginRequiredMixin, ListView):
    model = Korisnik
    template_name = 'listStudenti.html'
    context_object_name = 'studenti_list'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        student_role = Role.objects.get(role=Role.STUDENT)
        students = Korisnik.objects.filter(role=student_role)
        context['studenti_list'] = students
        return context
    

class ProfesoriListView(LoginRequiredMixin, ListView):
    model = Korisnik
    template_name = 'listProfesori.html'
    context_object_name = 'profesori_list'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profesorRole = Role.objects.get(role=Role.PROFESOR)
        profesors = Korisnik.objects.filter(role=profesorRole)
        context['profesori_list'] = profesors
        return context

class ProfesoriUpdateView(LoginRequiredMixin, UpdateView):
    model = Korisnik
    fields = ['username']
    template_name = 'editProfesor.html'
    success_url = '/list-profesori/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profesor'] = self.get_object()
        return context

class UserCreateView(LoginRequiredMixin, View):
     login_url = '/login/'
     redirect_field_name = 'redirect_to'
     def get(self, request):
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        form = UserForm()
        return render(request, 'createUser.html', {'form': form})

     def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = user.role.role
            print("ROLA: "+role)
            if role == 'STUDENT':
                return redirect('listStudenti')
            elif role == 'PROFESOR':
                return redirect('listProfesori')
            return redirect('listStudenti')
        return render(request, 'createUser.html', {'form': form})

class StudentiUpdateView(LoginRequiredMixin, UpdateView):
    model = Korisnik
    fields = ['username', 'status']
    template_name = 'studentEdit.html'
    success_url = '/list-studenti/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'ADMIN':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.get_object() 
        return context
    


class EnrollSubjectView(View): 
    def post(self, request, predmet_id, student_id):
        predmet = Predmeti.objects.get(pk=predmet_id)
        student = Korisnik.objects.get(pk=student_id)
        Upisi.objects.create(studentId=student, predmetId=predmet, status='upisan')
        return redirect('upisniList', student_id=student_id)

class DerollSubjectView(View):
    def post(self, request, predmet_id, student_id):
        predmet = Predmeti.objects.get(pk=predmet_id)
        student = Korisnik.objects.get(pk=student_id)

        Upisi.objects.filter(studentId=student, predmetId=predmet).delete()
        return redirect('upisniList', student_id=student_id)



class UpisaniStudentiView(LoginRequiredMixin, View):
    def get(self, request, predmet_id):
        predmet = get_object_or_404(Predmeti, pk=predmet_id)
        upisaniStudenti = Korisnik.objects.filter(student__predmetId=predmet).distinct()
        
        studenti_list = []
        for student in upisaniStudenti:
            statusPredmeta = Upisi.objects.filter(studentId=student.id, predmetId=predmet.id).values_list('status', flat=True).first()
            studenti_list.append((student, statusPredmeta))

        context = {
            'predmet': predmet,
            'studenti_list': studenti_list
        }
        return render(request, 'upisaniStudenti.html', context)




def update_status_predmeta(request, pk, predmet_id):
    if request.method == 'POST':
        status_predmeta = request.POST.get('statusPredmeta')
        student = get_object_or_404(Korisnik, pk=pk)
        predmet = get_object_or_404(Predmeti, pk=predmet_id)
        upisi = Upisi.objects.filter(studentId=student, predmetId=predmet)
        for upis in upisi:
            upis.status = status_predmeta
            upis.save()
    return redirect('upisaniStudenti', predmet_id=predmet_id)


class PredmetiProfesoriListView(LoginRequiredMixin, ListView):
    model = Predmeti
    template_name = 'listPredmetiProfesora.html'
    context_object_name = 'predmeti_list'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role.role != 'PROFESOR':
            return HttpResponseForbidden("Access Denied")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Predmeti.objects.filter(nositelj=self.request.user)