from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import RegisterData, Owners, CarSpecs


# Create your views here.
@login_required(login_url='login')
def display(request):
    cars = RegisterData.objects.all()
    paginator = Paginator(cars, 30)  # Show 30 contacts per page.
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
