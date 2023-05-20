import re
from datetime import date, timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.db.models import Q
from django.forms import ModelForm

from .models import RegisterData, Cars, Owners, CarSpecs


class CertificateRenewalForm(ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RegisterData
        fields = ['expiry_date', 'register_center']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Renew'))

    def save(self, commit=True):
        certificate = super(CertificateRenewalForm, self).save(commit=False)
        if commit:
            certificate.certificate_date = date.today()
            certificate.save()
        return certificate


class CertificateForm(ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    license_plate = forms.CharField(max_length=9, required=True)
    owner_name = forms.CharField(max_length=100, required=True)
    make = forms.CharField(max_length=100, required=True)
    model = forms.CharField(max_length=100, required=True)
    type = forms.ChoiceField(choices=[('Individual', 'Individual'), ('Company', 'Company')], required=True)
    address = forms.CharField(max_length=200, required=True)
    city = forms.ChoiceField(choices=[('Hà Nội', 'Hà Nội'), ('Hồ Chí Minh', 'Hồ Chí Minh'), ('Đà Nẵng', 'Đà Nẵng'),
                                      ('Hải Phòng', 'Hải Phòng'), ('Cần Thơ', 'Cần Thơ'), ('An Giang', 'An Giang'),
                                      ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu')],
                             required=True)
    phone_number = forms.CharField(max_length=10, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.add_input(Submit('submit', 'Register'))

    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        pattern = re.compile(r'^[0-9]{2}[A-Z]{1}-[0-9]{5}$')
        if not pattern.match(license_plate):
            raise forms.ValidationError("License Plate is not valid")
        if Cars.objects.filter(license_plate=license_plate).exists():
            raise forms.ValidationError("License Plate already exists")
        return license_plate

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        if expiry_date - date.today() < timedelta(days=365):
            raise forms.ValidationError("Expiry Date is not valid")
        return expiry_date

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pattern = re.compile(r'^[0-9]{10}$')
        if not pattern.match(phone_number):
            raise forms.ValidationError("Phone Number is not valid")
        return phone_number

    def save(self, commit=True):
        certificate = super().save(commit=False)
        owner = Owners.objects.get_or_create(name=self.cleaned_data["owner_name"], type=self.cleaned_data["type"],
                                      address=self.cleaned_data["address"], city_province=self.cleaned_data["city"],
                                      phone=self.cleaned_data["phone_number"])[0]
        car = Cars.objects.create(license_plate=self.cleaned_data["license_plate"], model_id=CarSpecs.objects.get(
            Q(make=self.cleaned_data["make"]) & Q(model=self.cleaned_data["model"])).id)
        certificate.license_plate = car
        certificate.certificate_date = date.today()
        certificate.owner = owner
        if commit:
            certificate.save()
        return certificate

    class Meta:
        model = RegisterData
        fields = ['expiry_date']
