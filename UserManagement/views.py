from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from Registration.models import RegisterData
from .forms import RegisterForm


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.has_perm('UserManagement.add_user'):
        context = {
            'user': request.user,
            'number_registered_by_month': RegisterData.objects.values('certificate_date__year',
                                                                      'certificate_date__month').annotate(
                count=Count('certificate_date__month')).order_by('certificate_date__year', 'certificate_date__month'),
            'number_expired_by_month': RegisterData.objects.values('expiry_date__year',
                                                                   'expiry_date__month').annotate(
                count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')[:12],
        }
    else:
        context = {'user': request.user,
                   'number_registered_by_month': RegisterData.objects.filter(
                       register_center__user_id=request.user.id).values('certificate_date__year',
                                                                        'certificate_date__month').annotate(
                       count=Count('certificate_date__month')).order_by('certificate_date__year',
                                                                        'certificate_date__month'),
                   'number_expired_by_month': RegisterData.objects.filter(
                       register_center__user_id=request.user.id).values('expiry_date__year',
                                                                        'expiry_date__month').annotate(
                       count=Count('expiry_date__month')).order_by('expiry_date__year', 'expiry_date__month')
                   }
    return render(request, 'partials/index.html', context)


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
    return render(request=request, template_name="partials/login.html", context={"form": form})


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
            messages.success(request, f'User created successfully.')
            form = RegisterForm()
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'partials/register.html', context)


def check_username(request):
    form = RegisterForm(request.GET)
    return HttpResponse(as_crispy_field(form['username']))


def check_register_center(request):
    form = RegisterForm(request.GET)
    return HttpResponse(as_crispy_field(form['register_center']))
