"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from datetime import date
import logging
from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from gwells.models import ProvinceStateCode
from wells.models import Well, ActivitySubmission, Casing, Screen, LinerPerforation, LithologyDescription, FieldsProvided
from submissions.models import WellActivityCode
from wells.stack import StackWells, overlap, merge_series
from registries.models import Person


logger = logging.getLogger(__name__)


class OverlapTest(TestCase):

    def test_overlap(self):
        # 0-1 ; 1-2 ; does not overlap.
        self.assertFalse(overlap((0, 1), (1, 2)))

    def test_overlap(self):
        # 0-1 ; 0-1 ; does overlap.
        self.assertTrue(overlap((0, 1), (0, 1)))

    def test_overlap(self):
        # 0-2 ; 1-2 ; does overlap.
        self.assertTrue(overlap((0, 2), (1, 2)))

    def test_overlap(self):
        # 0-2 ; 1-3 ; does overlap.
        self.assertTrue(overlap((0, 2), (1, 3)))


class SeriesMergeTest(TestCase):

    def test_new_data(self):
        # Test scenario where there is only new data.
        prev = []
        incoming = [
            {
                "id": 1,
                "from_": 0,
                "to": 10
            },
            {
                "id": 2,
                "from_": 10,
                "to": 20
            }
        ]
        expected = incoming
        new = merge_series(prev, incoming)
        self.assertEqual(new, expected)

    def test_no_overlap(self):
        # Test scenario where there is new and old data, but no overlap.
        prev = [
            {
                "id": 1,
                "start": 0,
                "end": 10
            },
        ]
        incoming = [
            {
                "id": 2,
                "start": 10,
                "end": 20
            },
        ]
        expected = [
            {
                "id": 1,
                "start": 0,
                "end": 10
            },
            {
                "id": 2,
                "start": 10,
                "end": 20
            },
        ]
        new = merge_series(prev, incoming)
        self.assertEqual(new, expected)

    def test_overlap(self):
        # Test scenario where there is overlap
        prev = [
            {
                "id": 1,
                "start": 0,
                "end": 10
            },
            {
                "id": 3,
                "start": 10,
                "end": 20
            },
        ]
        incoming = [
            {
                "id": 2,
                "start": 0,
                "end": 10
            },
        ]
        expected = [
            {
                "id": 2,
                "start": 0,
                "end": 10
            },
            {
                "id": 3,
                "start": 10,
                "end": 20
            },
        ]
        new = merge_series(prev, incoming)
        self.assertEqual(new, expected)

    def test_intersection(self):
        # Test scenario where there is intersection
        prev = [
            {
                "id": 1,
                "start": 0,
                "end": 10
            },
            {
                "id": 3,
                "start": 10,
                "end": 20
            },
        ]
        incoming = [
            {
                "id": 2,
                "start": 5,
                "end": 15
            },
        ]
        expected = [
            {
                "id": 2,
                "start": 5,
                "end": 15
            },
        ]
        new = merge_series(prev, incoming)
        self.assertEqual(new, expected)


def errors_side_effect(*args, **kwargs):
    return []


def is_valid_side_effect(*args, **kwargs):
    return False


class StackTest(TestCase):

    fixtures = ['wellsearch-codetables.json', ]

    def setUp(self):
        self.driller = Person.objects.create(
            first_name='Bobby',
            surname='Driller'
        )

        self.province = ProvinceStateCode.objects.get_or_create(
            province_state_code='BC',
            description='British Columbia',
            display_order=1
        )[0]

    def test_new_submission_gets_well_tag_number(self):
        # Test that when a constrction submission is processed, it is asigned a well_tag_number
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name='Bob',
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.construction(),
        )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        submission = ActivitySubmission.objects.get(filing_number=submission.filing_number)
        self.assertEqual(well.well_tag_number, submission.well.well_tag_number)

    def test_construction_submission_no_current_well(self):
        # Creating a brand new well that we only have a construction submission for.
        owner_full_name = 'Bob'
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=owner_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.construction(),
        )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(owner_full_name, well.owner_full_name)

    def test_alteration_after_construction(self):
        # Create a brand new well with a construction
        owner_full_name = 'Bob'
        new_owner_full_name = 'Joe'
        construction = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=owner_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.construction(),
        )
        stacker = StackWells()
        well = stacker.process(construction.filing_number)
        # Update the well with an alteration
        alteration = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=new_owner_full_name,
            work_start_date=date(2018, 2, 1),
            work_end_date=date(2018, 3, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.alteration(),
            well=well
        )
        well = stacker.process(alteration.filing_number)
        self.assertEqual(new_owner_full_name, well.owner_full_name)

    def test_alteration_submission_to_legacy_well(self):
        # The well already exists, but has no construction submission.
        original_full_name = 'Bob'
        new_full_name = 'Jimbo'
        # This is the original well record
        well = Well.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=original_full_name,
            owner_province_state=self.province,
            construction_start_date=date(2017, 1, 1),
            construction_end_date=date(2017, 1, 2))
        Casing.objects.create(start=0, end=10, well=well)
        Casing.objects.create(start=10, end=20, well=well)
        Screen.objects.create(start=0, end=10, well=well)
        Screen.objects.create(start=10, end=20, well=well)
        LinerPerforation.objects.create(start=0, end=10, well=well)
        LinerPerforation.objects.create(start=10, end=10, well=well)
        # Create a submission
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=new_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.alteration(),
            well=well
        )

        stacker = StackWells()
        stacker.process(submission.filing_number)
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        submissions = ActivitySubmission.objects.filter(well=well).order_by('work_start_date')
        # There should be two submissions at this point.
        # Submission 1: A legacy well submission generated using the original well record.
        # Submission 2: The submission for an alteration.
        self.assertEqual(submissions.count(), 2, "It is expected that a legacy submission be created")
        self.assertEqual(new_full_name, well.owner_full_name)
        # Test that all foreign key sets have also been copied
        self.assertEqual(submissions[0].casing_set.count(), 2, "It is expected that the casings on the "
                                                               "original well make part of the legacy "
                                                               "submission")
        self.assertEqual(submissions[0].screen_set.count(), 2, "It is expected that the screens on the "
                                                               "original well make part of the legacy "
                                                               "submission")
        self.assertEqual(submissions[0].linerperforation_set.count(), 2, "It is expected that the liner "
                                                                         "perforations on the original well "
                                                                         "make part of the legacy submission")
        self.assertEqual(
            submissions[0].work_start_date,
            well.construction_start_date,
            "It is expected that the well date match the submission date")
        self.assertEqual(
            submissions[0].work_end_date,
            well.construction_end_date,
            "Is it expected that the well date match the submission date")

    def test_construction_submission_to_legacy_well(self):
        # The well already exists, and we're applying a construction submission to it.
        # We're expecting a legacy record to be created, since we don't want to lose and information
        # that may already be in the well. Furthermore, we expect the construction submission to be applied
        # AFTER the legacy submission when stacking.
        original_full_name = 'Bob'
        new_full_name = 'Jimbo'
        # This is the original well record.
        well = Well.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=original_full_name,
            owner_province_state=self.province)
        # Create a submission.
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=new_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.construction(),
            well=well
        )

        stacker = StackWells()
        stacker.process(submission.filing_number)

        # Load all the submissions.
        submissions = ActivitySubmission.objects.filter(well=well)
        # Load the updated well record.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(submissions.count(), 2, "It is expected that a legacy submission be created")
        self.assertEqual(new_full_name, well.owner_full_name)

    def test_decomission_submission_to_legacy_well(self):
        # The well already exists, and we are applying a decommission submission to it.
        original_full_name = 'Bob'
        new_full_name = 'Jimbo'
        # This is the original well record.
        well = Well.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=original_full_name,
            owner_province_state=self.province)
        # Create a submission.
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=new_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.decommission(),
            well=well
        )

        stacker = StackWells()
        stacker.process(submission.filing_number)

        # Load all the submissions.
        submissions = ActivitySubmission.objects.filter(well=well)
        # Load the updated well record.
        well = Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(submissions.count(), 2, "It is expected that a legacy submission be created")
        self.assertEqual(new_full_name, well.owner_full_name)

    def test_construction_field_mapping(self):
        # Fields such as "work_start_date" on a construction report, need to map to "construction_start_date"
        # on a well.
        start_date = date(2018, 1, 1)
        end_date = date(2018, 1, 2)
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            work_start_date=start_date,
            work_end_date=end_date,
            well_activity_type=WellActivityCode.types.construction(),
        )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(start_date, well.construction_start_date)
        self.assertEqual(end_date, well.construction_end_date)

    def test_alteration_field_mapping(self):
        # Fields such as "work_start_date" on an alteration report, need to map to "alteration_start_date"
        # on a well.
        start_date = date(2018, 1, 1)
        end_date = date(2018, 1, 2)
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            work_start_date=start_date,
            work_end_date=end_date,
            well_activity_type=WellActivityCode.types.alteration(),
        )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(start_date, well.alteration_start_date)
        self.assertEqual(end_date, well.alteration_end_date)

    def test_decommission_field_mapping(self):
        # Fields such as "work_start_date" on a decommission report, need to map to "decommission_start_date"
        # on a well.
        start_date = date(2018, 1, 1)
        end_date = date(2018, 1, 2)
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            work_start_date=start_date,
            work_end_date=end_date,
            well_activity_type=WellActivityCode.types.decommission(),
        )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)
        Well.objects.get(well_tag_number=well.well_tag_number)
        self.assertEqual(start_date, well.decommission_start_date)
        self.assertEqual(end_date, well.decommission_end_date)

    def test_edit_comes_after_construction(self):
        # Stacking only works when done in the correct order. It's important that construction/legacy
        # submissions get processed 1st, and that alterations and edits get stacked on top of that.
        # In this case, we're creating a construction, and then applying an edit. We need to check
        # that the edit is applied over the construction.
        original_full_name = 'Bob'
        new_full_name = 'Jimbo'
        # Create a construction submission.
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=original_full_name,
            work_start_date=date(2018, 1, 1),
            work_end_date=date(2018, 2, 1),
            person_responsible=self.driller,
            owner_province_state=self.province,
            well_activity_type=WellActivityCode.types.construction()
        )
        stacker = StackWells()
        well = stacker.process(submission.filing_number)

        # Create an edit submission.
        submission = ActivitySubmission.objects.create(
            create_user='Something',
            update_user='Something',
            owner_full_name=new_full_name,
            well=well,
            well_activity_type=WellActivityCode.types.staff_edit()
        )

        FieldsProvided.objects.create(activity_submission=submission)

        stacker = StackWells()
        well = stacker.process(submission.filing_number)

        self.assertEqual(new_full_name, well.owner_full_name)

    @patch('wells.stack.submissions.serializers.WellSubmissionLegacySerializer.is_valid',
           side_effect=is_valid_side_effect)
    @patch('wells.stack.submissions.serializers.WellSubmissionLegacySerializer.errors',
           side_effect=errors_side_effect)
    def test_failure_to_generate_legacy_results_in_server_error(self, errors, is_valid):
        # We don't want failures to generate a legacy well to bubble up to client 400 errors, so we need
        # to make sure it's caught, and re-thrown as 500.
        # 1) Create the legacy well:
        well = Well.objects.create(
            create_user='Something',
            update_user='Something')
        # 2) Create the alteration:
        submission = ActivitySubmission.objects.create(
            well=well,
            create_user='Something',
            update_user='Something',
            well_activity_type=WellActivityCode.types.alteration())
        # 3) Attempt to stack:
        stacker = StackWells()
        # Assert that an exception is throw
        with self.assertRaises(APIException):
            try:
                stacker.process(submission.filing_number)
            except APIException as e:
                # Assert that it's a 500 error.
                self.assertEqual(e.status_code, HTTP_500_INTERNAL_SERVER_ERROR)
                # Re-raise the exception, handing it to the assertRaises above.
                raise
