from easyvalidator import rule_factory

class JsonValidator():
    def __init__(self, template, source):
        super().__init__()
        self.template = template
        self.source = source
        self.validation_result = None

    def validate(self):
        self.validation_result = self.analyse(
            self.template, source=self.source)
        return self.validation_result

    def has_error(self, result=None):
        if result is None:
            result = self.validation_result
        return "FAIL" in str(result)

    def find_value(self, property, source):
        return source[property] if property in source else None

    def property_not_found(self):
        return None

    def default_situation(self, field, source, rules: list):
        found_value = self.find_value(field, source)
        return {field: {"value": found_value, "rules": rules, "validations": self.apply_rules(rules, found_value)}}

    def apply_rules(self, rules: list, value):
        result = {}
        for rule_declaration in rules:
            rule = rule_factory.create_rule(rule_declaration)
            apply_result = rule.apply(value)
            result[rule_declaration] = apply_result
        return result

    def analyse(self, template: dict, source: dict):
        result = {}
        for field in template:
            rules = template[field]
            if type(rules) == str:
                rules = rules.split(".")
            if field not in source:
                result[field] = self.property_not_found()
            else:
                template_field_value = template[field]
                property_type = type(template_field_value)

                if property_type == dict:
                    source_field_value = source[field]
                    source_field_value_type = type(source_field_value)
                    if source_field_value_type == list:
                        result[field] = []
                        for source_from_array in source_field_value:
                            result[field].append(self.analyse(
                                template_field_value, source_from_array))
                    else:
                        source_field_value = source[field]
                        result[field] = self.analyse(
                            template_field_value, source_field_value)
                elif property_type == list:
                    source_field_value = source[field]
                    result[field] = []
                    for array_template in template_field_value:
                        if type(array_template) == dict:
                            for source_from_array in source_field_value:
                                result[field].append(self.analyse(
                                    array_template, source_from_array))
                        else:
                            result = self.default_situation(
                                field, source, rules)
                else:
                    result = self.default_situation(field, source, rules)
        return result
