from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import RegisterData, Owners, CarSpecs


# Create your views here.
@login_required(login_url='login')
def display(request):
    if request.GET.get('search'):
        search_item = request.GET.get('search')
        cars = RegisterData.objects.filter(Q(owner__name__icontains=search_item) |
                                           Q(license_plate__license_plate__icontains=search_item) |
                                           Q(license_plate__model__make__icontains=search_item) |
                                           Q(license_plate__model__model__icontains=search_item)
        )
    else:
        cars = RegisterData.objects.all()
    paginator = Paginator(cars, 20)  # Show 20 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'display.html', context)


@login_required(login_url='login')
def owner(request, owner_id):
    owner_data = Owners.objects.all()
    if owner_id is not None:
        owner_data = owner_data.filter(owner_id=owner_id)
    context = {'owners': owner_data}
    return render(request, 'owner.html', context)


@login_required(login_url='login')
def car_models(request):
    cars = CarSpecs.objects.all()
    context = {'cars': cars}
    return render(request, 'cars.html', context)


def car_detail(request, car_id):
    car_model = CarSpecs.objects.get(id=car_id)
    context = {'car': car_model}
    return render(request, 'car_detail.html', context)
