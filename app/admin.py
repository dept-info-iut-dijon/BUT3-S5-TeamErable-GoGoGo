from django.contrib import admin
from app.models import Personne
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class PersonneProfile(admin.StackedInline):

    model = Personne 



class UserAdmin(UserAdmin):

    inlines = (PersonneProfile,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)