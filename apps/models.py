from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import os

# Create your models here.
cities = [
    "Adilabad",
    "Bhadradri Kothagudem",
    "Hanamkonda",
    "Hyderabad",
    "Jagitial",
    "Jangaon",
    "Jayashankar Bhupalpally",
    "Jogulamba Gadwal",
    "Kamareddy",
    "Karimnagar",
    "Khammam",
    "Komaram Bheem Asifabad",
    "Mahabubabad",
    "Mahabubnagar",
    "Mancherial",
    "Medak",
    "Medchal–Malkajgiri",
    "Mulugu",
    "Nagarkurnool",
    "Nalgonda",
    "Narayanpet",
    "Nirmal",
    "Nizamabad",
    "Peddapalli",
    "Rajanna Sircilla",
    "Ranga Reddy",
    "Sangareddy",
    "Siddipet",
    "Suryapet",
    "Vikarabad",
    "Wanaparthy",
    "Warangal",
    "Yadadri Bhuvanagiri",
]
blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

CITY_CHOICES = [(city, city) for city in cities]
BLOOD_TYPES = [(blood, blood) for blood in blood_types]


class PersonalDetails(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=200)
    phone = models.IntegerField()
    place = models.CharField(max_length=33, choices=CITY_CHOICES)
    dob = models.DateField(verbose_name="Date Of Birth")
    blood_group = models.CharField(max_length=10, choices=BLOOD_TYPES)

    def __str__(self):
        return f"{self.fullname} ({self.user.username})"


class BloodRequired(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prescription = models.ImageField(upload_to="images/")
    patient_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=33, choices=CITY_CHOICES)
    hospital_name = models.CharField(max_length=200)
    blood_req = models.CharField(max_length=10, choices=BLOOD_TYPES)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    comments = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
