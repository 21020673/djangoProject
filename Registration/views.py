from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import RegisterData, Owners, CarSpecs

from django.views.generic import ListView


class ContactListView(ListView):
    paginate_by = 2
    model = RegisterData


# Create your views here.
@login_required(login_url='login')
def display(request):
    cars = RegisterData.objects.all()
    paginator = Paginator(cars, 30)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'display.html', context)


@login_required()
def owner(request):
    owner_data = Owners.objects.all()
    context = {'owners': owner_data}
    return render(request, 'owner.html', context)


@login_required()
def car_models(request):
    car_model = CarSpecs.objects.all()
    context = {'cars': car_model}
    return render(request, 'cars.html', context)
