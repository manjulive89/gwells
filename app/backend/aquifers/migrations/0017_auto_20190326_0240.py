# Generated by Django 2.1.7 on 2019-03-26 02:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0001_squashed_0069_auto_20190409_1634'),
        ('aquifers', '0001_squashed_0018_auto_20190409_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterRightsLicence',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('update_user', models.CharField(
                    default='DATALOAD_USER', max_length=60)),
                ('update_date', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('aquifer_licence_id', models.AutoField(primary_key=True,
                                                        serialize=False, verbose_name='Aquifer ID Number')),
                ('licence_number', models.BigIntegerField(db_index=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=3,
                                                 max_digits=12, null=True, verbose_name='Quanitity')),
                ('effective_date', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Aquifer Licences',
            },
        ),
        migrations.CreateModel(
            name='WaterRightsPurpose',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('update_user', models.CharField(
                    default='DATALOAD_USER', max_length=60)),
                ('update_date', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('code', models.CharField(db_column='water_rights_purpose_code',
                                          max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.PositiveIntegerField()),
                ('effective_date', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(
                    9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc))),
            ],
            options={
                'verbose_name_plural': 'Water Rights Purpose Codes',
                'db_table': 'water_rights_purpose_code',
                'ordering': ['display_order', 'code'],
            },
        ),
        migrations.AddField(
            model_name='waterrightslicence',
            name='purpose',
            field=models.ForeignKey(blank=True, db_column='water_rights_purpose_code', null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='licences', to='aquifers.WaterRightsPurpose', verbose_name='Water Rights Purpose Reference'),
        ),
        migrations.AddField(
            model_name='waterrightslicence',
            name='well',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='licences', to='wells.Well'),
        ),
    ]
