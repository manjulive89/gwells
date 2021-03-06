# Generated by Django 2.2.3 on 2019-07-24 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0101_merge_20190624_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='licenced_status',
            field=models.ForeignKey(db_column='licenced_status_code', default='UNLICENSED', on_delete=django.db.models.deletion.PROTECT, to='wells.LicencedStatusCode', verbose_name='Licensed Status'),
        ),
    ]
