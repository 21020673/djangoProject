import csv
import re
from datetime import date, timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Div
from django import forms
from django.db.models import Q
from django.forms import ModelForm
from django.urls import reverse_lazy

from .models import RegisterData, Cars, Owners, CarSpecs, RegisterCenter


class CertificateRenewalForm(ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RegisterData
        fields = ['expiry_date', 'register_center']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'renew-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('renew-certificate', kwargs={'certificate_id': self.instance.id}),
            'hx-target': '#renew-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.layout = Layout(Field('expiry_date'), Field('register_center'),
                                    HTML('<button class="btn btn-primary">Renew</button>'),
                                    )

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        if expiry_date - date.today() < timedelta(days=365):
            raise forms.ValidationError("Expiry Date is not valid")
        return expiry_date

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
    make_choices = [(make, make) for make in CarSpecs.objects.values_list('make', flat=True).distinct()]
    make = forms.ChoiceField(choices=make_choices, required=True, widget=forms.Select(
        attrs={'hx-get': reverse_lazy('get-models'), 'hx-target': '#models_select', 'hx-trigger': 'change'}))
    model = forms.CharField(required=True, widget=forms.Select(attrs={'id': 'models_select'}))
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
        self.helper.form_id = 'certificate-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('register-certificate'),
            'hx-target': '#certificate-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.layout = Layout(Div(Field('license_plate'), Field('expiry_date'), Field('owner_name'),
                                        Field('make'), Field('model'), Field('type'), Field('address'),
                                        Field('city'), Field('phone_number'), css_class='md:grid grid-cols-2 gap-x-10'),
                                    HTML('<button class="btn btn-primary">Submit</button>'))

    def clean_license_plate(self):
        license_plate = self.cleaned_data['license_plate']
        pattern = re.compile(r'^[0-9]{2}[A-Z]-[0-9]{5}$')
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

    def clean_model(self):
        model = self.cleaned_data['model']
        if not CarSpecs.objects.filter(model=model).exists():
            raise forms.ValidationError("Model is not valid")
        return model

    def save(self, commit=True):
        certificate = super().save(commit=False)
        owner = Owners.objects.get_or_create(name=self.cleaned_data["owner_name"], type=self.cleaned_data["type"],
                                             address=self.cleaned_data["address"],
                                             city_province=self.cleaned_data["city"],
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


class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv', 'class': 'file-input w-full max-w-md'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'upload-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('upload'),
            'hx-target': '#upload-form',
            'hx-swap': 'outerHTML',
            'enctype': 'multipart/form-data',
        }
        self.helper.layout = Layout(Field('file'), HTML('<button class="btn btn-primary">Upload</button>'))

    def clean_file(self):
        id_list = []
        csv_file = self.cleaned_data['file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File is not a CSV file')
        # Read the CSV file
        try:
            data = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(data)
            next(reader)
            for row in reader:
                register_center = RegisterCenter.objects.get(id=row[0])
                car = Cars.objects.get_or_create(license_plate=row[1])[0]
                car.model_id = row[2]
                car.save()
                temp = RegisterData.objects.filter(license_plate__license_plate=row[1])
                if temp.count() > 0:
                    temp.delete()
                owner = Owners.objects.get_or_create(name=row[3], type=row[4], phone=row[5], address=row[6],
                                                     city_province=row[7])[0]
                register_data = RegisterData.objects.get_or_create(register_center=register_center,
                                                                   license_plate=car, owner=owner,
                                                                   certificate_date=row[8],
                                                                   expiry_date=row[9])[0]
                id_list.append(register_data.id)
        except csv.Error as e:
            raise forms.ValidationError(e)
        return id_list
