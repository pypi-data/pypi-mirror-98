def is_null(value):
    return value is None

def is_not_null(value):
    return value is not None

def is_not_empty(value):
    return is_not_null(value) and len(value) > 0

def is_empty(value):
    return is_null(value) or len(value) == 0

def read_wargs(field, default=None, **kwargs):
    return kwargs[field] if field in kwargs else default


