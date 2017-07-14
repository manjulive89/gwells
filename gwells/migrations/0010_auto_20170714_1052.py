# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-14 17:52
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0009_auto_20170711_1600_squashed_0010_auto_20170713_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Casing',
            fields=[
                ('who_created', models.CharField(max_length=30)),
                ('when_created', models.DateTimeField(blank=True, null=True)),
                ('who_updated', models.CharField(max_length=30)),
                ('when_updated', models.DateTimeField(blank=True, null=True)),
                ('casing_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('casing_from', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='From')),
                ('casing_to', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='To')),
                ('internal_diameter', models.DecimalField(decimal_places=3, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.5'))], verbose_name='Diameter')),
                ('wall_thickness', models.DecimalField(decimal_places=3, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.5'))], verbose_name='Wall Thickness')),
                ('drive_shoe', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Drive Shoe')),
                ('activity_submission', models.ForeignKey(blank=True, db_column='filing_number', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.ActivitySubmission')),
            ],
            options={
                'db_table': 'gwells_casing',
            },
        ),
        migrations.CreateModel(
            name='CasingMaterial',
            fields=[
                ('who_created', models.CharField(max_length=30)),
                ('when_created', models.DateTimeField(blank=True, null=True)),
                ('who_updated', models.CharField(max_length=30)),
                ('when_updated', models.DateTimeField(blank=True, null=True)),
                ('casing_material_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('is_hidden', models.BooleanField(default=False)),
                ('sort_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'gwells_casing_material',
                'ordering': ['sort_order', 'description'],
            },
        ),
        migrations.CreateModel(
            name='CasingType',
            fields=[
                ('who_created', models.CharField(max_length=30)),
                ('when_created', models.DateTimeField(blank=True, null=True)),
                ('who_updated', models.CharField(max_length=30)),
                ('when_updated', models.DateTimeField(blank=True, null=True)),
                ('casing_type_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('is_hidden', models.BooleanField(default=False)),
                ('sort_order', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'gwells_casing_type',
                'ordering': ['sort_order', 'description'],
            },
        ),
        migrations.AddField(
            model_name='casing',
            name='casing_material',
            field=models.ForeignKey(blank=True, db_column='casing_material_guid', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.CasingMaterial', verbose_name='Casing Material'),
        ),
        migrations.AddField(
            model_name='casing',
            name='casing_type',
            field=models.ForeignKey(db_column='casing_type_guid', on_delete=django.db.models.deletion.CASCADE, to='gwells.CasingType', verbose_name='Casing Type'),
        ),
        migrations.AddField(
            model_name='casing',
            name='well',
            field=models.ForeignKey(blank=True, db_column='well_tag_number', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.Well'),
        ),
    ]