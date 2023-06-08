from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):

    ADMIN = 'ADMIN'
    PROFESOR =  'PROFESOR'
    STUDENT  = 'STUDENT'
    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (PROFESOR, 'profesor'),
        (STUDENT, 'student')
    ]

    role = models.CharField(choices=ROLE_CHOICES, max_length=50)

    """ def __str__(self):
        return '%s %s' % (self.user.username, self.role) """


class Korisnik(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL,blank=True, null=True, related_name="rola" )
    statusi = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    status = models.CharField(max_length=50, choices=statusi)




class Predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.SET_NULL, blank=True, null=True, related_name='nositelj')

    def __str__(self):
        return '%s %s' % (self.name, self.izborni)

class Upisi(models.Model):
    studentId = models.ForeignKey(Korisnik, on_delete=models.CASCADE, blank=True, null=True, related_name='student')
    predmetId = models.ForeignKey(Predmeti, on_delete=models.CASCADE, blank=True, null=True, related_name='predmet')
    status = (
        ('upisan', 'Upisan'),
        ('polozen', 'Polozen'),
        ('izgubio', 'IzgubioPotpis')
    )
    status=models.CharField(max_length=64, choices=status)



