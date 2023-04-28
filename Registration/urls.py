from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterDataView.as_view(), name='database'),
    path('owner/<int:owner_id>/', views.owner, name='owner'),
    path('owner/', views.OwnerView.as_view(), name='owner'),
    path('car/<pk>/', views.CarDetail.as_view(), name='car_detail'),
    path('cars/', views.CarsView.as_view(), name='cars'),
]