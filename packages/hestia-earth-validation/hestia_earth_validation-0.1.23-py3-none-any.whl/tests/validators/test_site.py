import unittest
import json
from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.site import validate_site, validate_site_dates, validate_site_coordinates, \
    validate_siteType


class TestValidatorsSite(unittest.TestCase):
    def test_validate_valid(self):
        with open(f"{fixtures_path}/site/valid.json") as f:
            node = json.load(f)
        self.assertListEqual(validate_site(node), [True] * 14)

    def test_validate_site_dates_valid(self):
        site = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-02'
        }
        self.assertEqual(validate_site_dates(site), True)

    def test_validate_site_dates_invalid(self):
        site = {
            'startDate': '2020-01-02',
            'endDate': '2020-01-01'
        }
        self.assertEqual(validate_site_dates(site), {
            'level': 'error',
            'dataPath': '.endDate',
            'message': 'must be greater than startDate'
        })

    def test_need_validate_coordinates(self):
        site = {'siteType': SiteSiteType.CROPLAND.value}
        self.assertEqual(validate_site_coordinates(site), False)
        site['latitude'] = 0
        site['longitude'] = 0
        self.assertEqual(validate_site_coordinates(site), True)
        site['siteType'] = SiteSiteType.AQUACULTURE_PENS
        self.assertEqual(validate_site_coordinates(site), False)

    def test_validate_siteType_valid(self):
        site = {
            'siteType': SiteSiteType.FOREST.value,
            'latitude': 44.18753,
            'longitude': -0.62521
        }
        self.assertEqual(validate_siteType(site), True)

        site = {
            'siteType': SiteSiteType.CROPLAND.value,
            'latitude': 44.5096,
            'longitude': 0.40749
        }
        self.assertEqual(validate_siteType(site), True)

    def test_validate_siteType_invalid(self):
        site = {
            'siteType': SiteSiteType.CROPLAND.value,
            'latitude': 44.18753,
            'longitude': -0.62521
        }
        self.assertEqual(validate_siteType(site), {
            'level': 'warning',
            'dataPath': '.siteType',
            'message': 'The coordinates you have provided are not in a known cropland '
            'area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands 25, 35, 36).'
        })

        site = {
            'siteType': SiteSiteType.FOREST.value,
            'latitude': 44.5096,
            'longitude': 0.40749
        }
        self.assertEqual(validate_siteType(site), {
            'level': 'warning',
            'dataPath': '.siteType',
            'message': 'The coordinates you have provided are not in a known forest '
            'area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands 10, 20, 25).'
        })
