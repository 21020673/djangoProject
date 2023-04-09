# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CarSpecs(models.Model):
    make = models.CharField(primary_key=True, max_length=45)
    model = models.CharField(max_length=200)
    generation = models.CharField(max_length=45)
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
        managed = False
        app_label = 'car_db'
        db_table = 'car_specs'
        unique_together = (('make', 'model', 'generation'),)


class Cars(models.Model):
    license_plate = models.CharField(primary_key=True, max_length=20)
    make = models.ForeignKey(CarSpecs, models.DO_NOTHING, db_column='make', blank=True, null=True,
                             related_name='car_make')
    model = models.ForeignKey(CarSpecs, models.DO_NOTHING, db_column='model', blank=True, null=True,
                              related_name='car_model')
    generation = models.ForeignKey(CarSpecs, models.DO_NOTHING, db_column='generation', blank=True, null=True,
                                   related_name='car_generation')

    class Meta:
        managed = False
        app_label = 'car_db'
        db_table = 'cars'


class Owners(models.Model):
    owner_id = models.CharField(primary_key=True, max_length=45)
    type = models.CharField(max_length=40, blank=True, null=True)
    cccd = models.CharField(db_column='CCCD', max_length=12, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    residence = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'car_db'
        db_table = 'owners'


class RegisterData(models.Model):
    certificate_id = models.IntegerField(primary_key=True)
    certificate_date = models.CharField(max_length=45, blank=True, null=True)
    expiry_date = models.CharField(max_length=45, blank=True, null=True)
    register_center = models.CharField(max_length=45, blank=True, null=True)
    owner = models.ForeignKey(Owners, models.DO_NOTHING, db_column='owner', blank=True, null=True)
    license_plate = models.ForeignKey(Cars, models.DO_NOTHING, db_column='license_plate', blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'car_db'
        db_table = 'register_data'

class CarRouter:
    """
    A router to control all database operations on models in the
    user application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to users_db.
        """
        if model._meta.app_label == 'car_db':
            return 'car'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write user models go to users_db.
        """
        if model._meta.app_label == 'car_db':
            return 'car'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the user app is involved.
        """
        if obj1._meta.app_label == 'car_db' or \
                obj2._meta.app_label == 'car_db':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'users_db'
        database.
        """
        if app_label == 'car_db':
            return db == 'car'
        return None
