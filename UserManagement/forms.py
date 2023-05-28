from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from Registration.models import RegisterCenter


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'register-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('register'),
            'hx-target': '#register-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.layout = Layout(
            Div(Field('username'),
                Field('email', wrapper_class='order-3'),
                Field('password1', wrapper_class='order-5'),
                Field('password2', wrapper_class='order-7'),
                Field('register_center', wrapper_class='order-2'),
                Field('city', wrapper_class='order-4'),
                Field('address', wrapper_class='order-6'),
                css_class='md:grid grid-cols-2 gap-x-10'),
            HTML('<button class="btn btn-primary">Register</button>'),
        )

    register_center = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={
            'hx-get': reverse_lazy('check-register-center'),
            'hx-target': '#div_id_register_center',
            'hx-trigger': 'keyup[target.value.length > 1] changed delay:1s'
        }
    ))
    address = forms.CharField(max_length=200, required=True)
    city = forms.ChoiceField(choices=[('Hà Nội', 'Hà Nội'), ('Hồ Chí Minh', 'Hồ Chí Minh'), ('Đà Nẵng', 'Đà Nẵng'),
                                      ('Hải Phòng', 'Hải Phòng'), ('Cần Thơ', 'Cần Thơ'), ('An Giang', 'An Giang'),
                                      ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu')],
                             required=True)

    class Meta:
        model = User
        fields = ["username", "register_center", "email", "city", "password1", "address", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-username'),
                'hx-target': '#div_id_username',
                'hx-trigger': 'keyup[target.value.length > 1] changed delay:1s',
            }),
        }

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            register_center = RegisterCenter(name=self.cleaned_data["register_center"],
                                             address=self.cleaned_data["address"],
                                             city_province=self.cleaned_data["city"], user=user)
            register_center.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username

    def clean_register_center(self):
        register_center = self.cleaned_data['register_center']
        if RegisterCenter.objects.filter(name=register_center).exists():
            raise forms.ValidationError("Register Center already exists")
        return register_center
