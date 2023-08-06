from easyvalidator.base_functions import *
from datetime import datetime

class BaseRule():
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.msg = read_wargs("msg", **kwargs)

    def apply(self, value):
        pass

class NotNull(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "Field can not be null" if self.msg is None else self.msg

    def apply(self, value):
        if is_not_null(value):
            return {"status": "OK"}
        return {"status": "FAIL", "msg": self.msg}

class NotEmpty(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "Field can not be empty" if self.msg is None else self.msg

    def apply(self, value):

        if is_not_empty(value) > 0:
            return {"status": "OK"}
        return {"status": "FAIL", "msg": self.msg}

class IsEmpty(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "Field shoul be empty" if self.msg is None else self.msg

    def apply(self, value):

        if is_empty(value):
            return {"status": "OK"}
        return {"status": "FAIL", "msg": self.msg}

class NotEquals(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", default=None, **kwargs)

    def apply(self, value):
        if self.value == value:
            return {"status": "FAIL", "msg": f"value can not be equals: {self.value}"}
        return {"status": "OK"}

class IsBetween(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = float(read_wargs(field="start", **kwargs))
        self.end = float(read_wargs(field="end", **kwargs))

    def apply(self, value):
        if self.start is None or self.end is None:
            return {"status": "FAIL", "msg": "start and end arguments can not be null"}

        value = float(value)

        if not (self.start < value < self.end):
            return {"status": "FAIL", "msg": f"value: {value} is not between start: {self.start} and end: {self.end}"}

        return {"status": "OK"}

class IsNotBetween(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = float(read_wargs(field="start", **kwargs))
        self.end = float(read_wargs(field="end", **kwargs))

    def apply(self, value):
        if self.start is None or self.end is None:
            return {"status": "FAIL", "msg": "start and end arguments can not be null"}

        value = float(value)

        if (self.start < value < self.end):
            return {"status": "FAIL", "msg": f"value: {value} is between start: {self.start} and end: {self.end}"}

        return {"status": "OK"}

class DateIsAfter(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = read_wargs(field="date", **kwargs)

    def apply(self, value):
        if value <= self.date:
            return {"status": "FAIL", "msg": f"date: {value} is not after: {self.date}"}
        return {"status": "OK"}

class DateIsBefore(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = read_wargs(field="date", **kwargs)

    def apply(self, value):
        if value >= self.date:
            return {"status": "FAIL", "msg": f"date: {value} is not before: {self.date}"}
        return {"status": "OK"}

class DateIsExactly(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = read_wargs(field="date", **kwargs)

    def apply(self, value):
        if value != self.date:
            return {"status": "FAIL", "msg": f"date: {value} is not exactly equals to: {self.date}"}
        return {"status": "OK"}

class GreaterThan(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if float(value) <= float(self.value):
            return {"status": "FAIL", "msg": f"value: {value} is not greater than: {self.value}"}
        return {"status": "OK"}

class LessThan(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if float(value) >= float(self.value):
            return {"status": "FAIL", "msg": f"value: {value} is not less than: {self.value}"}
        return {"status": "OK"}

class LessThanOrEqual(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if float(value) > float(self.value):
            return {"status": "FAIL", "msg": f"value: {value} is not less than or equals: {self.value}"}
        return {"status": "OK"}

class GreaterThanOrEqual(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if float(value) < float(self.value):
            return {"status": "FAIL", "msg": f"value: {value} is not greater than or equals: {self.value}"}
        return {"status": "OK"}

class TextEquals(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if value != self.value:
            return {"status": "FAIL", "msg": f"value: {value} is not equals: {self.value}"}
        return {"status": "OK"}

class TextContains(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if self.value not in value:
            return {"status": "FAIL", "msg": f"value: {value} does not contains: {self.value}"}
        return {"status": "OK"}

class TextNotContains(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if self.value in value:
            return {"status": "FAIL", "msg": f"value: {value} contains: {self.value}"}
        return {"status": "OK"}

class TextStartsWith(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if not value.startswith(self.value):
            return {"status": "FAIL", "msg": f"value: {value} not starts with: {self.value}"}
        return {"status": "OK"}

class TextEndsWith(BaseRule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = read_wargs(field="value", **kwargs)

    def apply(self, value):
        if not value.endswith(self.value):
            return {"status": "FAIL", "msg": f"value: {value} not ends with: {self.value}"}
        return {"status": "OK"}




