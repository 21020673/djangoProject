from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from .models import RegisterData, Owners, CarSpecs, RegisterCenter

city_list = RegisterCenter.objects.values_list('city_province', flat=True).distinct()
register_center_list = RegisterCenter.objects.values_list('name', flat=True).distinct()


# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class RegisterDataView(ListView):
    paginate_by = 9
    model = RegisterData
    template_name = 'register_data.html'

    def get_queryset(self):
        cars = RegisterData.objects.all()
        if self.request.GET.get('search'):
            search_item = self.request.GET.get('search')
            cars = RegisterData.objects.filter(Q(owner__name__icontains=search_item) |
                                               Q(license_plate__license_plate__icontains=search_item) |
                                               Q(license_plate__model__make__icontains=search_item) |
                                               Q(license_plate__model__model__icontains=search_item) |
                                               Q(register_center__city_province__icontains=search_item)
                                               )
        return cars


@method_decorator(login_required(login_url='login'), name='dispatch')
class OwnerView(ListView):
    paginate_by = 9
    model = Owners
    template_name = 'owner.html'

    def get_queryset(self):
        owners = Owners.objects.all()
        if self.request.GET.get('search'):
            search_item = self.request.GET.get('search')
            owners = Owners.objects.filter(Q(name__icontains=search_item) |
                                           Q(type__icontains=search_item) |
                                           Q(address__icontains=search_item) |
                                           Q(phone__icontains=search_item) |
                                           Q(city_province__icontains=search_item)
                                           )
        return owners


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarsView(ListView):
    paginate_by = 9
    model = CarSpecs
    template_name = 'cars.html'

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


@login_required(login_url='login')
def owner(request, owner_id):
    owner_data = Owners.objects.filter(owner_id=owner_id)
    context = {'page_obj': owner_data}
    return render(request, 'owner.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDetail(DetailView):
    model = CarSpecs
    template_name = 'car_detail.html'
    context_object_name = 'car'


def report_month(request):
    query = 'default'
    label = 'Number of cars registered in all areas'
    number_registered_by_month = RegisterData.objects.values('certificate_date__year',
                                                             'certificate_date__month').annotate(
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
    context = {
        'number_registered_by_month': number_registered_by_month,
        'cities': city_list,
        'register_centers': register_center_list,
        'label': label,
        'select': query
    }
    return render(request, 'graph.html', context)


def report_quarter(request):
    query = 'default'
    label = 'Number of cars registered in all areas'
    number_registered_by_quarter = RegisterData.objects.values('certificate_date__year',
                                                               'certificate_date__quarter').annotate(
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
    context = {
        'number_registered_by_quarter': number_registered_by_quarter,
        'cities': city_list,
        'register_centers': register_center_list,
        'label': label,
        'select': query
    }
    return render(request, 'graph.html', context)


def report_year(request):
    query = 'default'
    label = 'Number of cars registered in all areas'
    number_registered_by_year = RegisterData.objects.values('certificate_date__year').annotate(
        count=Count('certificate_date__year')).order_by('certificate_date__year')
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
    context = {
        'number_registered_by_year': number_registered_by_year,
        'cities': city_list,
        'register_centers': register_center_list,
        'label': label,
        'select': query
    }
    return render(request, 'graph.html', context)


def report_expiry(request):
    query = 'default'
    label = 'Number of certificates to expire in all areas'
    number_expired_by_month = RegisterData.objects.values('expiry_date__year', 'expiry_date__month').annotate(
        count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
    if request.GET.get('select'):
        query = request.GET.get('select')
        if query != 'default':
            label = 'Number of certificates to expire in ' + query
            if query in city_list:
                number_expired_by_month = RegisterData.objects.filter(register_center__city_province=query).values(
                    'expiry_date__year', 'expiry_date__month').annotate(
                    count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
            elif query in register_center_list:
                number_expired_by_month = RegisterData.objects.filter(register_center__name=query).values(
                    'expiry_date__year', 'expiry_date__month').annotate(
                    count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
    context = {
        'number_expired_by_month': number_expired_by_month[:12],
        'cities': city_list,
        'register_centers': register_center_list,
        'label': label,
        'select': query
    }
    return render(request, 'graph.html', context)
