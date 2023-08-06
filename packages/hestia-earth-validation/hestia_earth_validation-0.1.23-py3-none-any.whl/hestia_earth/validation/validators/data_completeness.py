def validate_dataCompleteness(data_completeness: dict):
    values = data_completeness.values()
    return next((value for value in values if isinstance(value, bool) and value is True), False) or {
        'level': 'warning',
        'dataPath': '.dataCompleteness',
        'message': 'may not all be set to false'
    }
