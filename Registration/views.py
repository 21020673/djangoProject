from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import RegisterData


# Create your views here.
@login_required(login_url='login')
def display(request):
    cars = RegisterData.objects.all()
    context = {'cars': cars}
    return render(request, 'display.html', context)
