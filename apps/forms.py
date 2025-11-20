from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["style"] = "height: 45px; border-radius: 10px;"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = PersonalDetails
        fields = ["fullname", "phone", "place", "dob", "blood_group"]


class RequirementForm(forms.ModelForm):
    class Meta:
        model = BloodRequired
        exclude = ["user", "created_at"]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control", "style": "height: 42px; border-radius: 8px;"}
            )

        # Fix for comments textarea
        self.fields["comments"].widget.attrs.update(
            {
                "rows": 3,
                "style": "height: auto; border-radius: 8px;",
                "placeholder": "Write any important notes for the donor or hospital...",
            }
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["style"] = "height: 45px; border-radius: 10px;"
