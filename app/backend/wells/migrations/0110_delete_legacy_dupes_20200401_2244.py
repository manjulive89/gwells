# Generated by Django 2.2.12 on 2020-04-01 22:44

from django.db import migrations, connection, transaction


SELECT_DUPLICATE_LEGACY_RECORDS = """
    SELECT MAX(filing_number) FROM activity_submission WHERE well_tag_number IN (
        SELECT well_tag_number
            FROM activity_submission
            WHERE well_activity_code='LEGACY'
            GROUP BY well_tag_number
            HAVING COUNT(*) > 1
            ORDER BY well_tag_number
    ) AND well_activity_code='LEGACY' GROUP BY well_tag_number ORDER BY well_tag_number;
"""


def delete_legacy_dupes(apps, schema_editor):
    ActivitySubmission = apps.get_model('wells', 'ActivitySubmission')

    with connection.cursor() as cursor:
        cursor.execute(SELECT_DUPLICATE_LEGACY_RECORDS)
        ids = [row[0] for row in cursor.fetchall()]

    print(f'Found {len(ids)} duplicate Legacy Activity Submissions')

    activity_submissions = ActivitySubmission.objects.filter(pk__in=ids)

    for activity_submission in activity_submissions:
        print(f'Deleting activity submission {activity_submission.filing_number}')
        try:
            delete_entire_submission(activity_submission)
        except Exception as e:
            print(f'Failed to delete activity submission')
            print(e)


@transaction.atomic
def delete_entire_submission(activity_submission):
    activity_submission.drilling_methods.clear()
    activity_submission.development_methods.clear()
    activity_submission.water_quality_characteristics.clear()

    activity_submission.lithologydescription_set.all().delete()
    activity_submission.casing_set.all().delete()
    activity_submission.decommission_description_set.all().delete()
    activity_submission.screen_set.all().delete()
    activity_submission.linerperforation_set.all().delete()

    activity_submission.fields_provided.delete()

    activity_submission.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('wells', '0109_positive_longitude_20200218_2310'),
    ]

    operations = [
        migrations.RunPython(delete_legacy_dupes),
    ]
