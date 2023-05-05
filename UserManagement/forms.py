from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Registration.models import RegisterCenter
from django import forms


class RegisterForm(UserCreationForm):
    register_center = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=200, required=True)
    city = forms.ChoiceField(choices=[('Hà Nội', 'Hà Nội'), ('Hồ Chí Minh', 'Hồ Chí Minh'), ('Đà Nẵng', 'Đà Nẵng'),
                                      ('Hải Phòng', 'Hải Phòng'), ('Cần Thơ', 'Cần Thơ'), ('An Giang', 'An Giang'),
                                      ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu')],
                             required=True)

    class Meta:
        model = User
        fields = ["username", "register_center", "email", "city", "password1", "address", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            RegisterCenter.objects.create(center_id=RegisterCenter.objects.count() + 1,
                                          name=self.cleaned_data["register_center"],
                                          address=self.cleaned_data["address"], city_province=self.cleaned_data["city"],
                                          user=user)
        return user
