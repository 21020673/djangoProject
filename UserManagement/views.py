from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.shortcuts import render, redirect

from Registration.models import RegisterData
from .forms import RegisterForm


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.has_perm('UserManagement.add_user'):
        context = {
            'user': request.user,
            'number_registered_by_year': RegisterData.objects.values('certificate_date__year').annotate(
                count=Count('certificate_date__year')).order_by('certificate_date__year'),
            'number_registered_by_month': RegisterData.objects.values('certificate_date__year',
                                                                      'certificate_date__month').annotate(
                count=Count('certificate_date__month')).order_by('certificate_date__year', 'certificate_date__month'),
            'number_expired_by_year': RegisterData.objects.values('expiry_date__year').annotate(
                count=Count('expiry_date__year')).order_by('expiry_date__year'),
            'number_expired_by_month': RegisterData.objects.values('expiry_date__year',
                                                                   'expiry_date__month').annotate(
                count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month'),
        }
    else:
        context = {'user': request.user}
    return render(request, 'index.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required(login_url='login')
@permission_required('UserManagement.add_user', raise_exception=True)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('register')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)
