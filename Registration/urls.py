from django.urls import path
from . import views

urlpatterns = [
    path('database/register_data/', views.RegisterDataView.as_view(), name='database'),
    path('database/owner/<int:owner_id>/', views.owner, name='owner'),
    path('database/owner/', views.OwnerView.as_view(), name='owner'),
    path('database/car/<pk>/', views.CarDetail.as_view(), name='car_detail'),
    path('database/cars/', views.CarsView.as_view(), name='cars'),
    path('report/month/', views.report_month, name='report_month'),
    path('report/quarter/', views.report_quarter, name='report_quarter'),
    path('report/year/', views.report_year, name='report_year'),
    path('report/expire/', views.report_expiry, name='report_expire'),
]