from typing import List
from functools import reduce
from statistics import mean


def _flatten(values: list): return list(reduce(lambda x, y: x + (y if isinstance(y, list) else [y]), values, []))


def _next_error(values: list): return next((x for x in values if x is not True), True)


def _filter_list_errors(values: list, return_single=True):
    values = list(filter(lambda x: x is not True, values))
    return True if return_single and len(values) == 0 else (values[0] if return_single and len(values) == 1 else values)


def _update_error_path(error: dict, key: str, index=None):
    path = f".{key}[{index}]{error.get('dataPath')}" if index is not None else f".{key}{error.get('dataPath')}"
    return {**error, **{'dataPath': path}}


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def _get_by_key(x, y):
    return x if x is None else (
        x.get(y) if isinstance(x, dict) else list(map(lambda v: _get_dict_key(v, y), x))
    )


def _get_dict_key(value: dict, key: str): return reduce(lambda x, y: _get_by_key(x, y), key.split('.'), value)


def _value_range_error(value: int, minimum: int, maximum: int):
    return 'minimum' if minimum is not None and value < minimum else \
        'maximum' if maximum is not None and value > maximum else False


def _list_has_props(values: List[dict], props: List[str]):
    return filter(lambda x: all(prop in x for prop in props), values)


def _list_sum(values: list, prop: str): return sum(map(lambda v: _safe_cast(v.get(prop, 0), float, 0.0), values))


def _filter_list(values: list, key: str, value): return list(filter(lambda v: _get_dict_key(v, key) == value, values))


def _compare_values(x, y):
    return next((True for item in x if item in y), False) if isinstance(x, list) and isinstance(y, list) else x == y


def _same_properties(value: dict, props: List[str]):
    def identical(test: dict):
        same_values = list(filter(lambda x: _compare_values(_get_dict_key(value, x), _get_dict_key(test, x)), props))
        return test if len(same_values) == len(props) else None
    return identical


def _average(value, default=0): return mean(value) if value is not None and isinstance(value, list) else default


def _value_average(node: dict, default=0):
    value = node.get('value')
    is_number = value is not None and (isinstance(value, float) or isinstance(value, int))
    return value if is_number else _average(value, default)
