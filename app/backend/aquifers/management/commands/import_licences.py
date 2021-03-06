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
import csv
import logging
import requests
from tempfile import NamedTemporaryFile

from django.core.management.base import BaseCommand
from django.conf import settings

from aquifers.models import WaterRightsLicence, WaterRightsPurpose, Aquifer
from wells.models import Well


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Downloads licences from DataBC and stores them locally.
    """

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, nargs="?", default=None,
                            help='The file to import. If not specified, download latest')
        parser.add_argument('-d', '--dev-fixtures', action='store_const', const=1,
                            help='Set this if you do not have a full production database, and only have dev fixtures.')

    def handle(self, *args, **options):
        if options['filename']:
            filename = options['filename']
        else:
            logging.info("Downloading licences from DataBC")
            input_file = NamedTemporaryFile(delete=False)
            url = "https://openmaps.gov.bc.ca/geo/pub/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&outputFormat=csv&typeNames=WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV&count=10000&cql_filter=POD_SUBTYPE NOT LIKE 'POD'"
            r = requests.get(url, allow_redirects=True)
            input_file.write(r.content)
            filename = input_file.name
            input_file.close()

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            # used in DEBUG mode only.
            counter = 0
            num_wells = Well.objects.count()

            # Delete all the water rights licenses as the WLS_WRL_SYSIDs can change (re: WATER-1115)
            WaterRightsLicence.objects.all().delete()

            use_dev_fixtures = options.get('dev_fixtures')

            # in dev envs, only import 100 licences.
            for row in reader:
                counter += 1
                well = None
                aquifer = None

                # If using dev_fixtures option then we limit the data for testng.
                if use_dev_fixtures:
                    if counter > 100:
                        break
                    well = Well.objects.all()[counter % num_wells:][0]
                    # We need our wells to actually have an aquifer for non-trivial testing.
                    if not well.aquifer:
                        well.aquifer = Aquifer.objects.first()
                        well.save()
                    aquifer = well.aquifer

                try:
                    self.process_row(row, use_dev_fixtures=use_dev_fixtures, well=well, aquifer=aquifer)
                except:
                    logger.exception('Error processing CSV row WLS_WRL_SYSID=%s', row['WLS_WRL_SYSID'])

    def process_row(self, row, use_dev_fixtures=False, well=None, aquifer=None):
        if row['POD_SUBTYPE'].strip() not in ['PWD', 'PG']:
            # [Nicole]: (we are only concerned with PWD and PG data – exclude any
            # rows with POD. POD refers to surface water which is out of scope for GWELLS)
            return

        if not row['SOURCE_NAME'].strip().isdigit():
            # Licence must be for an aquifer
            return

        if not row['WELL_TAG_NUMBER'].strip().isdigit():
            # Licence must be for a well
            return

        logging.info("importing licence #{}".format(row['LICENCE_NUMBER']))

        if not well or not aquifer:
            # Check the Licence is for a valid Aquifer and Well
            aquifer = Aquifer.objects.get(pk=row['SOURCE_NAME'])
            well = Well.objects.get(pk=row['WELL_TAG_NUMBER'])

        try:
            # Maintain code table with water rights purpose.
            purpose = WaterRightsPurpose.objects.get(
                code=row['PURPOSE_USE_CODE'].strip())
        except WaterRightsPurpose.DoesNotExist:
            purpose = WaterRightsPurpose.objects.create(
                code=row['PURPOSE_USE_CODE'].strip(),
                description=row['PURPOSE_USE'].strip())

        try:
            # Check to see if licence already exists in DB
            licence = WaterRightsLicence.objects.get(wrl_sysid=row['WLS_WRL_SYSID'])
        except WaterRightsLicence.DoesNotExist:
            licence = WaterRightsLicence(wrl_sysid=row['WLS_WRL_SYSID'])

        licence.licence_number = row['LICENCE_NUMBER'].strip()
        licence.quantity_flag = row['QUANTITY_FLAG'].strip()

        licence.purpose = purpose

        # Convert quantity to m3/year
        quantity = float(row['QUANTITY'].strip() or '0')
        if row['QUANTITY_UNITS'].strip() == "m3/sec":
            quantity = quantity * 60*60*24*365
        elif row['QUANTITY_UNITS'].strip() == "m3/day":
            quantity = quantity * 365
        elif row['QUANTITY_UNITS'].strip() == "m3/year":
            quantity = quantity
        else:
            raise Exception('unknown quantity unit: `{}`'.format(row['QUANTITY_UNITS']))

        licence.quantity = quantity
        licence.save()

        if not well.aquifer:
            well.aquifer = aquifer
        if licence not in well.licences.all():
            well.licences.add(licence)
        well.save()

        logging.info('assocated well={} aquifer={} licence_sysid={}'.format(
            well.pk,
            aquifer.pk,
            licence.pk
        ))

        return licence
