# Generated by Django 2.2.13 on 2020-06-19 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0115_update_well_class_indended_water_use_20200616_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='well_class',
            field=models.ForeignKey(blank=True, db_column='well_class_code', default='UNK', on_delete=django.db.models.deletion.PROTECT, to='wells.WellClassCode', verbose_name='Well Class'),
        ),
        migrations.AlterField(
            model_name='well',
            name='intended_water_use',
            field=models.ForeignKey(blank=True, db_column='intended_water_use_code', default='NA', on_delete=django.db.models.deletion.PROTECT, to='wells.IntendedWaterUseCode', verbose_name='Intended Water Use'),
        ),
    ]