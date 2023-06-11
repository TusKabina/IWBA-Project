"""
URL configuration for upisStudenata project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appUpisStudenata.views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
     path('login/', Login.as_view(), name='login'),
      #path('upisni-list/', UpisniListView.as_view(), name='upisniList'),
        path('upisni-list/<int:student_id>/', UpisniListView.as_view(), name='upisniList'),
      path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    #path('enroll/<int:pk>/', EnrollSubjectView.as_view(), name='enroll_subject'),
    #path('deroll/<int:pk>/', DerollSubjectView.as_view(), name='deroll_subject'),
    path('enroll/<int:predmet_id>/<int:student_id>/', EnrollSubjectView.as_view(), name='enroll_subject'),
path('deroll/<int:predmet_id>/<int:student_id>/', DerollSubjectView.as_view(), name='deroll_subject'),
    path('list-predmeti/', PredmetiListView.as_view(), name='listPredmeti'),
    path('predmeti/<int:pk>/edit/', PredmetiUpdateView.as_view(), name='editPredmeti'),
     path('createPredmet/', PredmetiCreateView.as_view(), name='createPredmet'),
     path('list-studenti/', StudentiListView.as_view(), name='listStudenti'),
     path('list-profesori/', ProfesoriListView.as_view(), name='listProfesori'),
    path('studenti/<int:pk>/edit/', StudentiUpdateView.as_view(), name='editStudent'),
    path('profesori/<int:pk>/edit/', ProfesoriUpdateView.as_view(), name='editProfesor'),
     path('createUser/', UserCreateView.as_view(), name='createUser'),
      path('predmet/<int:predmet_id>/studenti/', UpisaniStudentiView.as_view(), name='upisaniStudenti'),
       path('profesor/predmeti/', PredmetiProfesoriListView.as_view(), name='predmetiProfesora'),
       path('student/<int:pk>/update-status/<int:predmet_id>/', update_status_predmeta, name='updateStatusPredmeta'),
]
