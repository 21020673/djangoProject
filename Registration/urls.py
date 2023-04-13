from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='display'),
    path('owner/', views.owner, name='owner'),
    path('car/', views.car_models, name='car')
]