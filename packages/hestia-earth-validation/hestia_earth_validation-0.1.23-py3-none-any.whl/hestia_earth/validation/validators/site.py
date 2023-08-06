from hestia_earth.schema import SiteSiteType

from hestia_earth.validation.utils import _flatten
from hestia_earth.validation.gee import _fetch_data
from .shared import validate_dates, validate_list_dates, validate_list_duplicates, \
    validate_list_min_max, validate_region, validate_country, validate_coordinates, need_validate_coordinates, \
    validate_area, need_validate_area, validate_list_term_percent
from .infrastructure import validate_lifespan
from .measurement import validate_soilTexture, validate_depths, validate_value_min_max, validate_term_unique
from .practice import validate_cropResidueManagement


INLAND_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.POND.value,
    SiteSiteType.BUILDING.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value
]

SITE_TYPES_VALID_VALUES = {
    SiteSiteType.CROPLAND.value: [25, 35, 36],
    SiteSiteType.FOREST.value: [10, 20, 25]
}


def validate_site_dates(site: dict):
    return validate_dates(site) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_site_coordinates(site: dict):
    return need_validate_coordinates(site) and site.get('siteType') in INLAND_TYPES


def validate_siteType(site: dict):
    site_type = site.get('siteType')
    values = SITE_TYPES_VALID_VALUES[site_type] if site_type in SITE_TYPES_VALID_VALUES else []
    values_str = ', '.join(map(lambda v: str(v), values))

    def validate():
        value = _fetch_data(collection='MODIS/006/MCD12Q1',
                            ee_type='raster_by_period',
                            band_name='LC_Prop2',
                            year='2019',
                            latitude=site.get('latitude'),
                            longitude=site.get('longitude')).get('mean')
        return value in values

    return len(values) == 0 or validate() or {
        'level': 'warning',
        'dataPath': '.siteType',
        'message': ' '.join([
            'The coordinates you have provided are not in a known',
            site_type,
            f"area according to the MODIS Land Cover classification (MCD12Q1.006, LCCS2, bands {values_str})."
        ])
    }


def validate_site(site: dict):
    """
    Validates a single `Site`.

    Parameters
    ----------
    site : dict
        The `Site` to validate.

    Returns
    -------
    List
        The list of errors for the `Site`, which can be empty if no errors detected.
    """
    return [
        validate_site_dates(site),
        validate_siteType(site) if need_validate_coordinates(site) else True,
        validate_country(site) if 'country' in site else True,
        validate_region(site) if 'region' in site else True,
        validate_coordinates(site) if validate_site_coordinates(site) else True,
        validate_area(site) if need_validate_area(site) else True
    ] + _flatten([
        validate_list_dates(site, 'measurements'),
        validate_list_min_max(site, 'measurements'),
        validate_list_term_percent(site, 'measurements'),
        validate_soilTexture(site.get('measurements')),
        validate_depths(site.get('measurements')),
        validate_value_min_max(site.get('measurements')),
        validate_list_duplicates(site, 'measurements', [
            'term.@id',
            'method.@id',
            'methodDescription',
            'startDate',
            'endDate',
            'depthUpper',
            'depthLower'
        ]),
        validate_term_unique(site.get('measurements'))
    ] if 'measurements' in site else []) + _flatten([
        validate_list_dates(site, 'infrastructure'),
        validate_lifespan(site.get('infrastructure'))
    ] if 'infrastructure' in site else []) + _flatten([
        validate_list_dates(site, 'practices'),
        validate_list_min_max(site, 'practices'),
        validate_list_term_percent(site, 'practices'),
        validate_cropResidueManagement(site.get('practices'))
    ] if 'practices' in site else [])
