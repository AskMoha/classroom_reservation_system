from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from classroom_reservation_app.models import CustomUser
# Register your models here.

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)