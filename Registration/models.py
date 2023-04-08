from django.db import models


# Create your models here.
class Cars(models.Model):
    car_name = models.CharField(max_length=200)
    car_make = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200)
    car_year = models.CharField(max_length=200)

    def __str__(self):
        return self.car_name
class Owners(models.Model):
    owner_name = models.CharField(max_length=200)
    owner_car = models.ForeignKey(Cars, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner_name

class Resgisration(models.Model):
    car_name = models.ForeignKey(Cars, on_delete=models.CASCADE)
    owner_name = models.ForeignKey(Owners, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return self.car_name