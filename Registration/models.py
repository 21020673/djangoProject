# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class CarSpecs(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=45, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    generation = models.CharField(max_length=45, blank=True, null=True)
    year_from = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    year_to = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    series = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    body_type = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    number_of_seats = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    length_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    width_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    height_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    wheelbase_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    front_track_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    rear_track_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    curb_weight_kg = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    ground_clearance_mm = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    engine_type = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    engine_hp = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    transmission = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    maximum_torque_n_m = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    acceleration_0_100_km_h_s = models.CharField(db_column='acceleration_0_100_km/h_s', max_length=200,
                                                 db_collation='utf8_general_ci', blank=True,
                                                 null=True)  # Field renamed to remove unsuitable characters.
    max_speed_km_per_h = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    fuel_tank_capacity_l = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    city_fuel_per_100km_l = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)
    fuel_grade = models.CharField(max_length=200, db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        db_table = 'car_specs'


class Cars(models.Model):
    license_plate = models.CharField(primary_key=True, max_length=9)
    model = models.ForeignKey(CarSpecs, models.DO_NOTHING, blank=False, null=True)

    class Meta:
        db_table = 'cars'

    def __str__(self):
        return self.license_plate


class Owners(models.Model):
    type = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    city_province = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'owners'

    def __str__(self):
        return self.name


class RegisterCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city_province = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'register_center'

    def __str__(self):
        return "Trung tâm " + self.name


class RegisterData(models.Model):
    certificate_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=False, null=True)
    register_center = models.ForeignKey(RegisterCenter, models.DO_NOTHING, db_column='register_center', blank=False)
    owner = models.ForeignKey(Owners, models.DO_NOTHING, db_column='owner', blank=False)
    license_plate = models.ForeignKey(Cars, models.DO_NOTHING, db_column='license_plate', blank=False)

    class Meta:
        db_table = 'register_data'
