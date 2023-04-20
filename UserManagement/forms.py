from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Registration.models import RegisterCenter
from django import forms


class RegisterForm(UserCreationForm):
    register_center = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)
    city_province = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "register_center", "address", "city_province"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            RegisterCenter.objects.create(center_id=RegisterCenter.objects.count(),
                                                            name=self.cleaned_data["register_center"],
                                                            address=self.cleaned_data["address"],
                                                            city_province=self.cleaned_data["city_province"],
                                                            user=user)
        return user
