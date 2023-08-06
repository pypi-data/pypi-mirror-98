from hestia_earth.schema import SchemaType

from hestia_earth.validation.utils import _flatten, _update_error_path
from .shared import validate_empty_fields
from .cycle import validate_cycle
from .impact_assessment import validate_impact_assessment
from .organisation import validate_organisation
from .site import validate_site


VALIDATE_TYPE = {
    SchemaType.CYCLE.value: lambda v: validate_cycle(v),
    SchemaType.IMPACTASSESSMENT.value: lambda v: validate_impact_assessment(v),
    SchemaType.ORGANISATION.value: lambda v: validate_organisation(v),
    SchemaType.SITE.value: lambda v: validate_site(v)
}


def _validate_node_type(ntype: str, node: dict):
    validations = VALIDATE_TYPE[ntype](node) if ntype in VALIDATE_TYPE else []
    empty_warnings = validate_empty_fields(node)
    return validations + empty_warnings


def _validate_node_children(node: dict):
    validations = []
    for key, value in node.items():
        if isinstance(value, list):
            validations.extend([_validate_node_child(key, value, index) for index, value in enumerate(value)])
        if isinstance(value, dict):
            validations.append(_validate_node_child(key, value))
    return _flatten(validations)


def _validate_node_child(key: str, value: dict, index=None):
    values = validate_node(value)
    return list(map(lambda error: _update_error_path(error, key, index) if isinstance(error, dict) else error, values))


def validate_node(node: dict):
    """
    Validates a single Node.

    Parameters
    ----------
    node : dict
        The JSON-Node to validate.

    Returns
    -------
    List
        The list of errors/warnings for the node, which can be empty if no errors/warnings detected.
    """
    ntype = node.get('type') if isinstance(node, dict) else None
    return [] if ntype is None else list(filter(lambda v: v is not True, _flatten(
        _validate_node_type(ntype, node) + _validate_node_children(node)
    )))
