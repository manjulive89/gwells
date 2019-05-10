# Generated by Django 2.1.7 on 2019-04-18 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitysubmission',
            name='alteration_end_date',
            field=models.DateField(null=True, verbose_name='Alteration Date'),
        ),
        migrations.AddField(
            model_name='activitysubmission',
            name='alteration_start_date',
            field=models.DateField(null=True, verbose_name='Alteration Start Date'),
        ),
        migrations.AddField(
            model_name='activitysubmission',
            name='construction_end_date',
            field=models.DateField(null=True, verbose_name='Construction Date'),
        ),
        migrations.AddField(
            model_name='activitysubmission',
            name='construction_start_date',
            field=models.DateField(null=True, verbose_name='Construction Start Date'),
        ),
        migrations.AddField(
            model_name='activitysubmission',
            name='decommission_end_date',
            field=models.DateField(null=True, verbose_name='Decommission Date'),
        ),
        migrations.AddField(
            model_name='activitysubmission',
            name='decommission_start_date',
            field=models.DateField(null=True, verbose_name='Decommission Start Date'),
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='final_casing_stick_up',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='Final Casing Stick Up'),
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='water_supply_system_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Water Supply System Name'),
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='water_supply_system_well_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Water Supply System Well Name'),
        ),
    ]
