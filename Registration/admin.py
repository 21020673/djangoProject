from django.contrib import admin

# Register your models here.
from .models import CarSpecs, RegisterData, RegisterCenter, Owners, Cars

admin.site.register(CarSpecs)
admin.site.register(RegisterData)
admin.site.register(RegisterCenter)
admin.site.register(Owners)
admin.site.register(Cars)