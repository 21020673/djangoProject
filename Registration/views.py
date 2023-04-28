from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .models import RegisterData, Owners, CarSpecs


# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class RegisterDataView(ListView):
    paginate_by = 20
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
    paginate_by = 20
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
    paginate_by = 20
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
