from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(PersonalDetails)


@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ("fullname", "phone", "place", "blood_group")
    list_filter = ("blood_group",)
    search_field = ("fullname",)


@admin.register(BloodRequired)
class BloodRequiredAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "age", "blood_req", "hospital_name")
