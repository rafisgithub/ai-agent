
from django.contrib import admin
from unfold.admin import ModelAdmin
from . models import CustomUser


@admin.register(CustomUser)
class CustomAdminClass(ModelAdmin):
    model = CustomUser
    list_display = ("first_name", "last_name", "email", "is_staff", "is_active", "date_joined",)
    list_filter = ("first_name", "last_name", "email", "is_staff", "is_active",)
    


    search_fields = ("email",)
    ordering = ("email",)