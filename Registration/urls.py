from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='database'),
    path('owner/<int:owner_id>/', views.owner, name='owner'),
    path('owner/', views.owner, kwargs={'owner_id': None}, name='owner'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/', views.car_models, name='cars'),
]