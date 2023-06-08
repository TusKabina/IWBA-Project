from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Korisnik, Role, Predmeti, Upisi
# Register your models here.

admin.site.register(Role)

@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
    



admin.site.register(Predmeti)
admin.site.register(Upisi)