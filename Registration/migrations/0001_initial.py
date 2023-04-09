# Generated by Django 3.2.18 on 2023-04-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('license_plate', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'cars',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CarSpecs',
            fields=[
                ('make', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=200)),
                ('generation', models.CharField(max_length=45)),
                ('year_from', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('year_to', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('series', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('body_type', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('number_of_seats', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('length_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('width_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('height_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('wheelbase_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('front_track_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('rear_track_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('curb_weight_kg', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('ground_clearance_mm', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('engine_type', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('engine_hp', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('transmission', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('maximum_torque_n_m', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('acceleration_0_100_km_h_s', models.CharField(blank=True, db_collation='utf8_general_ci', db_column='acceleration_0_100_km/h_s', max_length=200, null=True)),
                ('max_speed_km_per_h', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('fuel_tank_capacity_l', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('city_fuel_per_100km_l', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
                ('fuel_grade', models.CharField(blank=True, db_collation='utf8_general_ci', max_length=200, null=True)),
            ],
            options={
                'db_table': 'car_specs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Owners',
            fields=[
                ('owner_id', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, max_length=40, null=True)),
                ('cccd', models.CharField(blank=True, db_column='CCCD', max_length=12, null=True)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('residence', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'owners',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterData',
            fields=[
                ('certificate_id', models.IntegerField(primary_key=True, serialize=False)),
                ('certificate_date', models.CharField(blank=True, max_length=45, null=True)),
                ('expiry_date', models.CharField(blank=True, max_length=45, null=True)),
                ('register_center', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'register_data',
                'managed': False,
            },
        ),
    ]
