import json
from datetime import date

import pandas as pd
from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from prophet import Prophet

from .forms import CertificateRenewalForm, CertificateForm, FileUploadForm
from .models import RegisterData, Owners, CarSpecs, RegisterCenter

city_list = RegisterCenter.objects.values_list('city_province', flat=True).distinct()
register_center_list = RegisterCenter.objects.values_list('name', flat=True).distinct()


# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class RegisterDataView(ListView):
    paginate_by = 10
    model = RegisterData

    def get_queryset(self):
        if self.request.user.has_perm('UserManagement.add_user'):
            objects = RegisterData.objects.all()
        else:
            objects = RegisterData.objects.filter(register_center__user_id=self.request.user.id)
        if self.request.GET.get('search'):
            search_item = self.request.GET.get('search')
            objects = objects.filter(Q(owner__name__icontains=search_item) |
                                     Q(license_plate__license_plate__icontains=search_item) |
                                     Q(register_center__city_province__icontains=search_item)
                                     )
        ordering = self.request.GET.get('sort')
        if ordering == 'month':
            objects = objects.filter(certificate_date__year=date.today().year,
                                     certificate_date__month=date.today().month)
        elif ordering == 'quarter':
            objects = objects.filter(certificate_date__year=date.today().year,
                                     certificate_date__month__gte=date.today().month - 3)
        elif ordering == 'year':
            objects = objects.filter(certificate_date__year=date.today().year)
        elif ordering == 'expire':
            objects = objects.filter(expiry_date__year=date.today().year, expiry_date__month=date.today().month)
        return objects

    def get_template_names(self):
        if self.request.META.get("HTTP_HX_REQUEST") == 'true':
            return ['partials/register_data.html']
        else:
            return ['register_data.html']


@method_decorator(login_required(login_url='login'), name='dispatch')
class OwnerView(ListView):
    paginate_by = 10
    model = Owners

    def get_queryset(self):
        if self.request.user.has_perm('UserManagement.add_user'):
            owners = Owners.objects.all()
        else:
            owners = Owners.objects.filter(registerdata__register_center__user_id=self.request.user.id)
        if self.request.GET.get('search'):
            search_item = self.request.GET.get('search')
            owners = owners.filter(Q(name__icontains=search_item) |
                                   Q(type__icontains=search_item) |
                                   Q(address__icontains=search_item) |
                                   Q(phone__icontains=search_item) |
                                   Q(city_province__icontains=search_item)
                                   )
        return owners

    def get_template_names(self):
        if self.request.META.get("HTTP_HX_REQUEST") == 'true':
            return ['partials/owner.html']
        else:
            return ['owner.html']


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarsView(ListView):
    paginate_by = 10
    model = CarSpecs

    def get_queryset(self):
        cars = CarSpecs.objects.all()
        if self.request.GET.get('search'):
            search_item = self.request.GET.get('search')
            cars = CarSpecs.objects.filter(Q(make__icontains=search_item) |
                                           Q(model__icontains=search_item) |
                                           Q(year_from__icontains=search_item) |
                                           Q(body_type__icontains=search_item)
                                           )
        return cars

    def get_template_names(self):
        if self.request.META.get("HTTP_HX_REQUEST") == 'true':
            return ['partials/cars.html']
        else:
            return ['cars.html']


@login_required(login_url='login')
def owner(request, owner_id):
    owner_data = Owners.objects.filter(id=owner_id)
    context = {'page_obj': owner_data}
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/owner.html', context)
    return render(request, 'owner.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDetail(DetailView):
    model = CarSpecs
    context_object_name = 'car'

    def get_template_names(self):
        if self.request.META.get("HTTP_HX_REQUEST") == 'true':
            return ['partials/car_detail.html']
        else:
            return ['car_detail.html']


def report_month(request):
    if request.user.has_perm('UserManagement.add_user'):
        label = 'Number of cars registered in all areas'
        number_registered_by_month = RegisterData.objects.values('certificate_date__year',
                                                                 'certificate_date__month').annotate(
            count=Count('certificate_date__month')).order_by('certificate_date__year', 'certificate_date__month')
    else:
        query = RegisterCenter.objects.get(user_id=request.user.id).name
        label = 'Number of cars registered in ' + query
        number_registered_by_month = RegisterData.objects.filter(register_center__name=query).values(
            'certificate_date__year', 'certificate_date__month').annotate(
            count=Count('certificate_date__month')).order_by('certificate_date__year', 'certificate_date__month')
    if request.GET.get('select'):
        query = request.GET.get('select')
        if query != 'default':
            label = 'Number of cars registered in ' + query
            if query in city_list:
                number_registered_by_month = RegisterData.objects.filter(register_center__city_province=query).values(
                    'certificate_date__year', 'certificate_date__month').annotate(
                    count=Count('certificate_date__month')).order_by('certificate_date__year',
                                                                     'certificate_date__month')
            elif query in register_center_list:
                number_registered_by_month = RegisterData.objects.filter(register_center__name=query).values(
                    'certificate_date__year', 'certificate_date__month').annotate(
                    count=Count('certificate_date__month')).order_by('certificate_date__year',
                                                                     'certificate_date__month')
    data = json.dumps({
        'data': [item['count'] for item in number_registered_by_month][-12:],
        'labels': ['T' + str(item['certificate_date__month']) + '-' + str(item['certificate_date__year']) for item in
                   number_registered_by_month][-12:],
        'label': label,
    })
    return HttpResponse(data, content_type='application/json')


def report_quarter(request):
    if request.user.has_perm('UserManagement.add_user'):
        label = 'Number of cars registered in all areas'
        number_registered_by_quarter = RegisterData.objects.values('certificate_date__year',
                                                                   'certificate_date__quarter').annotate(
            count=Count('certificate_date__quarter')).order_by('certificate_date__year', 'certificate_date__quarter')
    else:
        query = RegisterCenter.objects.get(user_id=request.user.id).name
        label = 'Number of cars registered in ' + query
        number_registered_by_quarter = RegisterData.objects.filter(register_center__name=query).values(
            'certificate_date__year', 'certificate_date__quarter').annotate(
            count=Count('certificate_date__quarter')).order_by('certificate_date__year', 'certificate_date__quarter')
    if request.GET.get('select'):
        query = request.GET.get('select')
        if query != 'default':
            label = 'Number of cars registered in ' + query
            if query in city_list:
                number_registered_by_quarter = RegisterData.objects.filter(
                    register_center__city_province=query).values(
                    'certificate_date__year', 'certificate_date__quarter').annotate(
                    count=Count('certificate_date__quarter')).order_by('certificate_date__year',
                                                                       'certificate_date__quarter')
            elif query in register_center_list:
                number_registered_by_quarter = RegisterData.objects.filter(register_center__name=query).values(
                    'certificate_date__year', 'certificate_date__quarter').annotate(
                    count=Count('certificate_date__quarter')).order_by('certificate_date__year',
                                                                       'certificate_date__quarter')
    data = json.dumps({
        'data': [item['count'] for item in number_registered_by_quarter][-12:],
        'labels': ['Q' + str(item['certificate_date__quarter']) + '-' + str(item['certificate_date__year']) for item in
                   number_registered_by_quarter][-12:],
        'label': label,
    })
    return HttpResponse(data, content_type='application/json')


def report_year(request):
    if request.user.has_perm('UserManagement.add_user'):
        label = 'Number of cars registered in all areas'
        number_registered_by_year = RegisterData.objects.values('certificate_date__year').annotate(
            count=Count('certificate_date__year')).order_by('certificate_date__year')
    else:
        query = RegisterCenter.objects.get(user_id=request.user.id).name
        label = 'Number of cars registered in ' + query
        number_registered_by_year = RegisterData.objects.filter(register_center__name=query).values(
            'certificate_date__year').annotate(count=Count('certificate_date__year')).order_by('certificate_date__year')
    if request.GET.get('select'):
        query = request.GET.get('select')
        if query != 'default':
            label = 'Number of cars registered in ' + query
            if query in city_list:
                number_registered_by_year = RegisterData.objects.filter(register_center__city_province=query).values(
                    'certificate_date__year').annotate(
                    count=Count('certificate_date__year')).order_by('certificate_date__year')
            elif query in register_center_list:
                number_registered_by_year = RegisterData.objects.filter(register_center__name=query).values(
                    'certificate_date__year').annotate(
                    count=Count('certificate_date__year')).order_by('certificate_date__year')
    data = json.dumps({
        'data': [item['count'] for item in number_registered_by_year],
        'labels': [str(item['certificate_date__year']) for item in number_registered_by_year],
        'label': label,
    })
    return HttpResponse(data, content_type='application/json')


def report_expiry(request):
    if request.user.has_perm('UserManagement.add_user'):
        label = 'Number of certificates expiring in all areas'
        number_expired_by_month = RegisterData.objects.values('expiry_date__year', 'expiry_date__month').annotate(
            count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
    else:
        query = RegisterCenter.objects.get(user_id=request.user.id).name
        label = 'Number of certificates expiring in ' + query
        number_expired_by_month = RegisterData.objects.filter(register_center__name=query).values(
            'expiry_date__year', 'expiry_date__month').annotate(count=Count('expiry_date__month')).order_by(
            'expiry_date__year', 'expiry_date__month')
    if request.GET.get('select'):
        query = request.GET.get('select')
        if query != 'default':
            label = 'Number of certificates expiring in ' + query
            if query in city_list:
                number_expired_by_month = RegisterData.objects.filter(register_center__city_province=query).values(
                    'expiry_date__year', 'expiry_date__month').annotate(
                    count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
            elif query in register_center_list:
                number_expired_by_month = RegisterData.objects.filter(register_center__name=query).values(
                    'expiry_date__year', 'expiry_date__month').annotate(
                    count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
    data = json.dumps({
        'data': [item['count'] for item in number_expired_by_month][:12],
        'labels': ['T' + str(item['expiry_date__month']) + '-' + str(item['expiry_date__year']) for item in
                   number_expired_by_month][:12],
        'label': label,
    })
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='login')
def renew_certificate(request, certificate_id):
    certificate = get_object_or_404(RegisterData, pk=certificate_id)
    if certificate.register_center.user_id != request.user.id:
        raise PermissionDenied
    if request.method == 'POST':
        form = CertificateRenewalForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate renewed successfully')
            return HttpResponse(status=204, headers={'HX-Trigger': 'reload'})
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
    else:
        form = CertificateRenewalForm(instance=certificate)
    context = {
        'form': form,
        'owner': certificate.owner.name,
        'license_plate': certificate.license_plate,
    }
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/renew_form.html', context)
    return render(request, 'renew_form.html', context)


@login_required(login_url='login')
def register_certificate(request):
    if request.user.has_perm('UserManagement.add_user'):
        raise PermissionDenied
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.register_center = RegisterCenter.objects.get(user_id=request.user.id)
            form.save()
            messages.success(request, 'Certificate registered successfully')
            return redirect('home')
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
    else:
        form = CertificateForm()
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/register.html', {'form': form, 'title': 'Register Certificate'})
    return render(request, 'register.html', {'form': form, 'title': 'Register Certificate'})


@login_required(login_url='login')
@permission_required('UserManagement.add_user', raise_exception=True)
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['upload_result'] = form.cleaned_data['file']
            messages.success(request, 'File uploaded successfully')
            return HttpResponse(status=204, headers={'HX-Trigger': 'upload-result'})
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
    else:
        form = FileUploadForm()
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/upload.html', {'form': form, 'title': 'Upload File'})
    return render(request, 'register.html', {'form': form, 'title': 'Upload File'})


@login_required(login_url='login')
@permission_required('UserManagement.add_user', raise_exception=True)
def upload_result(request):
    result = RegisterData.objects.filter(id__in=request.session['upload_result'])
    paginator = Paginator(result, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/upload_result.html', {'page_obj': page_obj})
    return render(request, 'upload_result.html', {'page_obj': page_obj})


def report(request):
    if request.user.has_perm('UserManagement.add_user'):
        query = 'default'
    else:
        query = RegisterCenter.objects.get(user_id=request.user.id).name
    context = {
        'cities': city_list,
        'register_centers': register_center_list,
        'select': query
    }
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/report.html', context)
    return render(request, 'report.html', context)


def predict(request):
    number_registered_by_month = RegisterData.objects.values('certificate_date').annotate(
        count=Count('certificate_date'))
    query = request.GET.get('select')
    if query != 'default':
        if query in city_list:
            number_registered_by_month = RegisterData.objects.filter(
                register_center__city_province=query).values('certificate_date').annotate(
                count=Count('certificate_date'))
        elif query in register_center_list:
            number_registered_by_month = RegisterData.objects.filter(register_center__name=query).values(
                'certificate_date').annotate(count=Count('certificate_date'))
    df = pd.DataFrame.from_records(number_registered_by_month).rename({'certificate_date': 'ds', 'count': 'y'}, axis=1)
    m = Prophet(seasonality_mode='multiplicative').fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future).groupby(pd.Grouper(key='ds', freq='M')).sum().reset_index()
    data = json.dumps({
        'data': [item['yhat'] for item in forecast.to_dict('records')][-24:],
        'labels': ['T' + str(item['ds'].month) + '-' + str(item['ds'].year) for item in forecast.to_dict('records')][
                  -24:],
    })
    return HttpResponse(data, content_type='application/json')


def get_models(request):
    make = request.GET.get('make')
    models = request.GET.get('model')
    if models:
        generations = CarSpecs.objects.filter(model=models).values_list('generation', flat=True).distinct()
        if request.META.get("HTTP_HX_REQUEST") == 'true':
            return render(request, 'partials/select_choices.html', {'choices': generations})
    else:
        models = CarSpecs.objects.filter(make=make).values_list('model', flat=True).distinct()
        if request.META.get("HTTP_HX_REQUEST") == 'true':
            return render(request, 'partials/select_choices.html', {'choices': models})
    return redirect('home')


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {'list_register': RegisterData.objects.filter(certificate_date__year=date.today().year,
                                                            certificate_date__month=date.today().month),

               'list_expired': RegisterData.objects.filter(expiry_date__year=date.today().year,
                                                           expiry_date__month=date.today().month),
               }
    if request.META.get("HTTP_HX_REQUEST") == 'true':
        return render(request, 'partials/index.html', context)
    return render(request, 'index.html', context)
