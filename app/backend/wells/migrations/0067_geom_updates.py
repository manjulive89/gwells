# Generated by Django 2.1.7 on 2019-03-18 22:57

from django.db import migrations
from django.core.exceptions import FieldDoesNotExist
import logging
logger = logging.getLogger(__name__)


def update_fields(apps, schema_editor):
    activitySubmission = apps.get_model('wells', 'activitysubmission')
    try:
        activitySubmission._meta.get_field('latitude')
        schema_editor.execute("update activity_submission set geom = ST_SetSrid(ST_MakePoint(longitude, latitude), 4326);")
    except FieldDoesNotExist:
        logger.error('Field does not exist.')

    well = apps.get_model('wells', 'well')
    try:
        well._meta.get_field('latitude')
        schema_editor.execute("update well set geom = ST_SetSrid(ST_MakePoint(longitude, latitude), 4326);")
    except FieldDoesNotExist:
        logger.error('Field does not exist.')


def reverse_update_fields(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0066_auto_20190318_2257'),
    ]

    operations = [
        migrations.RunPython(update_fields, reverse_code=reverse_update_fields),
        migrations.RemoveField(
            model_name='activitysubmission',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='activitysubmission',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='well',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='well',
            name='longitude',
        ),
    ]