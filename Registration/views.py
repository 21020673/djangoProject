from django.shortcuts import render
from django.shortcuts import render, redirect


# Create your views here.
def display(request):
    if request.user.is_authenticated:
        return render(request, 'display.html')
    else:
        return redirect('login')
