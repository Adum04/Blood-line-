from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

# Register Form


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created")
            return redirect("login")
        else:
            messages.error(request, "Invalid")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


# Login Function


def login_view(request):
    # it checks whether it is valid method or not
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["style"] = "height: 45px; border-radius: 8px;"
        # Here django is using email to authenticate as django field is still named username we check that
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Authenticate by inbuilt method using email
            user = authenticate(request, username=email, password=password)
            # if user is valid the login will be successfull
            if user:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect("dashboard")

            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()
        # To Apply Bootstrap Styling to Every Form Field and shape of form
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["style"] = "height: 45px; border-radius: 8px;"

    return render(request, "login.html", {"form": form})


# edit profile function


@login_required
def edit_profile(request):
    # get or create a profile for the current user
    profile, created = PersonalDetails.objects.get_or_create(
        user=request.user,
        defaults={
            "fullname": "",
            "phone": "",
            "place": "",
            "dob": "2000-01-01",
            "blood_group": "",
        },
    )

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile_view")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})


@login_required
def blood_requirement(request):
    try:
        profile = PersonalDetails.objects.get(user=request.user)
    except PersonalDetails.DoesNotExist:
        messages.error(
            request, "Please complete your profile before posting a blood requirement."
        )
        return redirect("edit_profile")

    # You can also ensure fields are not empty
    if not profile.phone or not profile.place or not profile.blood_group:
        messages.error(
            request, "Please complete your profile before posting a blood requirement."
        )
        return redirect("edit_profile")
    if request.method == "POST":
        form = RequirementForm(request.POST, request.FILES)
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.user = request.user
            requirement.save()
            messages.success(request, "Your blood requirement has been posted!")
            return redirect("dashboard")
        else:
            messages.error(request, "There was an error in the form.")
    else:
        form = RequirementForm()

    return render(request, "require.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


# @login_required
def dashboard(request):

    # Auto delete posts older than 1 minute (FOR TESTING)
    BloodRequired.objects.filter(
        created_at__lt=timezone.now() - timedelta(hours=48)
    ).delete()

    requirements_list = BloodRequired.objects.all().order_by("-id")
    paginator = Paginator(requirements_list, 6)
    page_number = request.GET.get("page")
    requirements = paginator.get_page(page_number)
    return render(request, "dashboard.html", {"requirements": requirements})


def about(request):
    return render(request, "about.html")


@login_required
def profile_view(request):
    # default profile
    profile, created = PersonalDetails.objects.get_or_create(
        user=request.user,
        defaults={
            "fullname": "",
            "phone": 0,
            "place": "",
            "dob": "2000-01-01",
            "blood_group": "",
        },
    )
    user_requirements = BloodRequired.objects.filter(user=request.user).order_by("-id")

    return render(
        request,
        "profile.html",
        {"profile": profile, "user_requirements": user_requirements},
    )


@login_required
def delete_requirement(request, id):
    requirement = get_object_or_404(BloodRequired, id=id, user=request.user)
    requirement.delete()
    messages.success(request, "Your blood requirement post has been deleted.")
    return redirect("profile_view")
