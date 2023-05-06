from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('check-username', views.check_username, name='check-username'),
]

htmx_urlpatterns = [
    path('check-username', views.check_username, name='check-username'),
    path('check-register-center', views.check_register_center, name='check-register-center'),
]

urlpatterns += htmx_urlpatterns
