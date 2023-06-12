from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from .forms import RegisterForm


# Create your views here.
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as {username}.")
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
    messages.success(request, "Successfully logged out.")
    return redirect('login')


@login_required(login_url='login')
@permission_required('UserManagement.add_user', raise_exception=True)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'User created successfully.')
            form = RegisterForm()
            return render(request, 'partials/register.html', {'form': form, 'title': 'Register new user'})
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
    else:
        form = RegisterForm()
        if request.META.get("HTTP_HX_REQUEST") == 'true':
            return render(request, 'partials/register.html', {'form': form, 'title': 'Register new user'})
        return render(request, 'register.html', {'form': form, 'title': 'Register new user'})


def check_username(request):
    form = RegisterForm(request.GET)
    return HttpResponse(as_crispy_field(form['username']))


def check_register_center(request):
    form = RegisterForm(request.GET)
    return HttpResponse(as_crispy_field(form['register_center']))
