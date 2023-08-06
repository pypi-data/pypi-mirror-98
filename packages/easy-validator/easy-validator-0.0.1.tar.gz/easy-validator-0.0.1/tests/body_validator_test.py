
from easyvalidator.validator import JsonValidator

def validate(template, source):           
    result = JsonValidator(template=template, source=source).validate()        
    return result

def test_not_null_status_ok():
    rule_name = "NotNull"
    source = { "name": "Test Name" }    
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "OK"

def test_not_null_status_fail():
    rule_name = "NotNull"
    source = { "name": None }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "FAIL"

def test_not_empty_status_ok():
    rule_name = "NotEmpty"
    source = { "name": " " }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "OK"

def test_not_empty_status_fail():
    rule_name = "NotEmpty"
    source = { "name": "" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "FAIL"

def test_is_empty_status_ok():
    rule_name = "IsEmpty"
    source = { "name": "" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "OK"

def test_is_empty_status_fail():
    rule_name = "IsEmpty"
    source = { "name": "not empty" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "FAIL"

def test_is_not_equals_status_ok():
    rule_name = "NotEquals(value=OBJ. C)"
    source = { "name": "PYTHON" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "OK"

def test_is_not_equals_status_fail():
    rule_name = "NotEquals(value=PYTHON)"
    source = { "name": "PYTHON" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "FAIL"

def test_is_not_equals_number_status_ok():
    rule_name = "NotEquals(value=7)"
    source = { "name": "PYTHON" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "OK"

def test_is_not_equals_number_status_fail():
    rule_name = "NotEquals(value=7)"
    source = { "name": "7" }
    template = { "name": [rule_name] }
    result = validate(template, source)
    assert result["name"]["validations"][rule_name]["status"] == "FAIL"

def test_is_between_status_ok():
    rule_name = "IsBetween(start=1, end=5)"
    source = { "age": 3 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_is_between_status_fail():
    rule_name = "IsBetween(start=10, end=18)"
    source = { "age": 3 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "FAIL"

def test_is_not_between_status_ok():
    rule_name = "IsNotBetween(start=1, end=5)"
    source = { "age": 7 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_is_not_between_status_fail():
    rule_name = "IsNotBetween(start=10, end=18)"
    source = { "age": 15 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "FAIL"

def test_date_is_after_status_ok():
    rule_name = "DateIsAfter(date=2019-01-01)"
    source = { "birthDate": "2020-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "OK"

def test_date_is_after_status_fail():
    rule_name = "DateIsAfter(date=2019-01-01)"
    source = { "birthDate": "2018-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "FAIL"

def test_date_is_after_same_date_status_fail():
    rule_name = "DateIsAfter(date=2019-01-01)"
    source = { "birthDate": "2019-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "FAIL"

def test_date_is_before_status_ok():
    rule_name = "DateIsBefore(date=2019-01-01)"
    source = { "birthDate": "2018-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "OK"

def test_date_is_before_status_fail():
    rule_name = "DateIsBefore(date=2019-01-01)"
    source = { "birthDate": "2020-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "FAIL"

def test_date_is_before_same_date_status_fail():
    rule_name = "DateIsBefore(date=2019-01-01)"
    source = { "birthDate": "2019-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "FAIL"

def test_date_is_exactly_status_ok():
    rule_name = "DateIsExactly(date=2019-01-01)"
    source = { "birthDate": "2019-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "OK"

def test_date_is_exactly_status_fail():
    rule_name = "DateIsExactly(date=2019-01-01)"
    source = { "birthDate": "2020-01-01" }
    template = { "birthDate": [rule_name] }
    result = validate(template, source)
    assert result["birthDate"]["validations"][rule_name]["status"] == "FAIL"

def test_value_is_greater_than_ok():
    rule_name = "GreaterThan(value=1)"
    source = { "age": 5 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_value_is_greater_than_fail():
    rule_name = "GreaterThan(value=10)"
    source = { "age": 5 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "FAIL"

def test_value_is_less_than_ok():
    rule_name = "LessThan(value=1152)"
    source = { "age": 1 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_value_is_less_than_fail():
    rule_name = "LessThan(value=10)"
    source = { "age": 500 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "FAIL"

def test_value_is_greater_than_or_equals_value_greater_ok():
    rule_name = "GreaterThanOrEqual(value=11)"
    source = { "age": 100 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_value_is_greater_than_or_equals_value_equals_ok():
    rule_name = "GreaterThanOrEqual(value=10)"
    source = { "age": 10 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_value_is_greater_than_or_equals_fail():
    rule_name = "GreaterThanOrEqual(value=10)"
    source = { "age": 5 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "FAIL"

def test_value_is_less_than_or_equals_value_less_ok():
    rule_name = "LessThanOrEqual(value=100)"
    source = { "age": 100 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_value_is_less_than_or_equals_value_equals_ok():
    rule_name = "LessThanOrEqual(value=10)"
    source = { "age": 10 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "OK"

def test_value_is_less_than_or_equals_fail():
    rule_name = "LessThanOrEqual(value=10)"
    source = { "age": 50 }
    template = { "age": [rule_name] }
    result = validate(template, source)
    assert result["age"]["validations"][rule_name]["status"] == "FAIL"

def test_value_is_equals_ok():
    rule_name = "TextEquals(value=BRWORKIT)"
    source = { "developer": "BRWORKIT" }
    template = { "developer": [rule_name] }
    result = validate(template, source)
    assert result["developer"]["validations"][rule_name]["status"] == "OK"

def test_value_is_equals_fail():
    rule_name = "TextEquals(value=BRWORKIT)"
    source = { "developer": "BRWORKIT 2" }
    template = { "developer": [rule_name] }
    result = validate(template, source)
    assert result["developer"]["validations"][rule_name]["status"] == "FAIL"

def test_value_contains_ok():
    rule_name = "TextContains(value=sp)"
    source = { "message": "I live in sp" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "OK"

def test_value_contains_fail():
    rule_name = "TextContains(value=sp)"
    source = { "message": "I live in ny" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "FAIL"

def test_value_not_contains_ok():
    rule_name = "TextNotContains(value=sp)"
    source = { "message": "I live in cd" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "OK"

def test_value_not_contains_fail():
    rule_name = "TextNotContains(value=sp)"
    source = { "message": "I live in sp" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "FAIL"

def test_value_starts_with_ok():
    rule_name = "TextStartsWith(value=I live)"
    source = { "message": "I live in cd" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "OK"

def test_value_starts_with_fail():
    rule_name = "TextStartsWith(value=You live)"
    source = { "message": "I live in cd" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "FAIL"

def test_value_ends_with_ok():
    rule_name = "TextEndsWith(value=my best place)"
    source = { "message": "I live in cd my best place" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "OK"

def test_value_ends_with_fail():
    rule_name = "TextEndsWith(value=You live)"
    source = { "message": "I live in cd" }
    template = { "message": [rule_name] }
    result = validate(template, source)
    assert result["message"]["validations"][rule_name]["status"] == "FAIL"

def test_has_error_ok():
    rule_name = "NotNull"
    source = { "message": None }
    template = { "message": [rule_name] }
    validator = JsonValidator(template=template, source=source)
    result = validator.validate()
    assert validator.has_error(result) == True