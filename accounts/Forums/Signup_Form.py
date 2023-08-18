from django import forms
from accounts.models import User
from django.contrib.auth.hashers import make_password
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email_address','password','age','profile_pic']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user        