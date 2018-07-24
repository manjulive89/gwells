# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-24 20:26
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('gwells', '0006_auto_20180724_2026'),
        ('wells', '0003_auto_20180724_0007'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='LithologyDescription',
            fields=[
                ('create_user', models.CharField(max_length=60)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('update_user', models.CharField(max_length=60, null=True)),
                ('update_date', models.DateTimeField(blank=True, null=True)),
                ('lithology_description_guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lithology_from', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='From')),
                ('lithology_to', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='To')),
                ('lithology_raw_data', models.CharField(blank=True, max_length=250, null=True, verbose_name='Raw Data')),
                ('water_bearing_estimated_flow', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Water Bearing Estimated Flow')),
                ('lithology_observation', models.CharField(blank=True, max_length=250, null=True, verbose_name='Observations')),
                ('lithology_sequence_number', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lithology_description',
                'ordering': ['lithology_sequence_number'],
            },
        ),
        migrations.AlterField(
            model_name='activitysubmission',
            name='well_activity_type',
            field=models.ForeignKey(db_column='well_activity_code', on_delete=django.db.models.deletion.CASCADE, to='submissions.WellActivityCode', verbose_name='Type of Work'),
        ),
        migrations.DeleteModel(
            name='WellActivityCode',
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='activity_submission',
            field=models.ForeignKey(blank=True, db_column='filing_number', null=True, on_delete=django.db.models.deletion.CASCADE, to='wells.ActivitySubmission'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='bedrock_material',
            field=models.ForeignKey(blank=True, db_column='bedrock_material_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.BedrockMaterialCode', verbose_name='Bedrock Material'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='bedrock_material_descriptor',
            field=models.ForeignKey(blank=True, db_column='bedrock_material_descriptor_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.BedrockMaterialDescriptorCode', verbose_name='Descriptor'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='lithology_colour',
            field=models.ForeignKey(blank=True, db_column='lithology_colour_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.LithologyColourCode', verbose_name='Colour'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='lithology_description',
            field=models.ForeignKey(blank=True, db_column='lithology_description_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.LithologyDescriptionCode', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='lithology_hardness',
            field=models.ForeignKey(blank=True, db_column='lithology_hardness_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.LithologyHardnessCode', verbose_name='Hardness'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='lithology_material',
            field=models.ForeignKey(blank=True, db_column='lithology_material_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.LithologyMaterialCode', verbose_name='Material'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='lithology_moisture',
            field=models.ForeignKey(blank=True, db_column='lithology_moisture_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.LithologyMoistureCode', verbose_name='Moisture'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='lithology_structure',
            field=models.ForeignKey(blank=True, db_column='lithology_structure_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='gwells.LithologyStructureCode', verbose_name='Bedding'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='secondary_surficial_material',
            field=models.ForeignKey(blank=True, db_column='secondary_surficial_material_code', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_surficial_material_set', to='gwells.SurficialMaterialCode', verbose_name='Secondary Surficial Material'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='surficial_material',
            field=models.ForeignKey(blank=True, db_column='surficial_material_code', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='surficial_material_set', to='gwells.SurficialMaterialCode', verbose_name='Surficial Material'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='water_bearing_estimated_flow_units',
            field=models.ForeignKey(blank=True, db_column='well_yield_unit_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='wells.WellYieldUnitCode', verbose_name='Units'),
        ),
        migrations.AddField(
            model_name='lithologydescription',
            name='well_tag_number',
            field=models.ForeignKey(blank=True, db_column='well_tag_number', null=True, on_delete=django.db.models.deletion.CASCADE, to='wells.Well'),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
