import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.data_completeness import validate_dataCompleteness


class TestValidatorsDataCompleteness(unittest.TestCase):
    def test_validate_dataCompleteness_valid(self):
        with open(f"{fixtures_path}/dataCompleteness/valid.json") as f:
            data = json.load(f)
        self.assertEqual(validate_dataCompleteness(data), True)

    def test_validate_dataCompleteness_warning(self):
        with open(f"{fixtures_path}/dataCompleteness/warning.json") as f:
            data = json.load(f)
        self.assertEqual(validate_dataCompleteness(data), {
            'level': 'warning',
            'dataPath': '.dataCompleteness',
            'message': 'may not all be set to false'
        })
