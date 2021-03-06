# Generated by Django 2.2.10 on 2020-02-18 23:10

from django.db import migrations

UPDATE_LONGITUDE = 'UPDATE well SET geom = ST_SetSRID(ST_MakePoint(-1 * ABS(ST_X(geom)), ST_Y(geom)), 4326) WHERE ST_X(geom) > -110;'

class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0108_auto_20200213_1741'),
    ]

    operations = [
        migrations.RunSQL(
            UPDATE_LONGITUDE,
        ),
    ]
