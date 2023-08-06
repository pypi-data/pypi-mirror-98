"""
This modules allows to modify the form between Fields validations and Form
validation.

When the tests (:class:`ConditionTest`) associated with a :class:`Condition`
are fulfilled, then an action is executed on a list of fields.

This can be used in the following situations:

- Conditional fields: remove fields (e.g. if a checkbox is not checked).
  See :class:`formidable.forms.conditions.DisplayIffCondition`
- Conditional access: change access level (required/editable/...)

.. autoclass:: Condition

.. autoclass:: ConditionTest
   :members: mapper

"""


class ConditionsRegister(dict):
    """
    Store actions used for `conditions`.
    It allows to convert a `conditions` schema into a list of `Condition`
    objects that will be used to apply _actions_ when the tests of the
    conditions are True.
    """

    def gen_from_schema(self, fields, conditions_schema):
        index = 0
        for condition in conditions_schema:
            index += 1
            # name, fields_ids, action, tests
            condition_class = self[condition['action']]

            # cast values to field's type
            def convert_values(field_id, values):
                try:
                    field = fields[field_id]
                except KeyError:
                    return []

                # Define that we have a multiple field or not.
                multiple = hasattr(field, "choices") and \
                    field.widget.allow_multiple_selected
                if multiple:
                    # Multiple fields accept lists only as values.
                    return field.to_python(values)
                else:
                    return [field.to_python(value) for value in values]

            tests = [ConditionTest(test['field_id'],
                                   test['operator'],
                                   convert_values(test['field_id'],
                                                  test['values']))
                     for test in condition['tests']]
            condition_name = condition.get('name') or '#{}'.format(index)
            yield condition_class(
                condition['fields_ids'],
                condition_name,
                tests
            )

    def build(self, fields, conditions_schema):
        return list(self.gen_from_schema(fields, conditions_schema))


conditions_register = ConditionsRegister()


class ConditionsMetaClass(type):
    """
    Metaclass that registers each Condition subclass into `conditions_register`
    """

    def __new__(mcls, name, base, attrs):
        condition_class = super().__new__(
            mcls, name, base, attrs
        )
        if 'action' in attrs:
            conditions_register[condition_class.action] = condition_class
        return condition_class


def operator_eq(ref_value, values):
    """
    Compare if the field values is in the condition values.
    """
    if isinstance(ref_value, list):
        for v in values:
            if v in ref_value:
                return True
    return ref_value == values[0]


class ConditionTest:
    """
    Test that is evaluated to know if the action of a :class:`Condition` can be
    applied.
    A test compare a field's value to a reference value using an operator
    defined in `mapper`
    """

    mapper = {'eq': operator_eq}

    def __init__(self, field_id, operator, values):
        self.field_id = field_id
        self.operator = operator
        # do we need to cast values according to ref field type ?
        # form.fields[field_id].to_python(value) ...
        self.values = values

    def __call__(self, cleaned_data):
        meth = self.mapper[self.operator]

        try:
            ref_value = cleaned_data[self.field_id]
        except KeyError:
            # KeyError if self.field_id not in cleaned_data
            # TODO XXX add log ?
            return False
        else:
            return meth(ref_value, self.values)

    def __repr__(self):
        return '<ConditionTest: {field} {operator} {values}>'.format(
            field=self.field_id,
            operator=self.operator,
            values=self.values
        )


class Condition(metaclass=ConditionsMetaClass):
    """
    Object that represents a Conditional action to be applied on some fields
    depending on the result of the `tests`.

    .. note:: This class needs to be specialized to implement the actions.
    """

    def __init__(self, fields_ids, name, tests):
        self.name = name
        self.tests = tests
        self.fields_ids = fields_ids

    def __repr__(self):
        return "<Condition {action}: {name}>".format(
            action=self.action,
            name=self.name)

    def keep_fields(self, cleaned_data):
        """
        Return ``True`` if the conditions require the fields to be displayed.
        """
        raise NotImplementedError(
            "The condition `{}` should have a `keep_fields` method".format(
                self.name))


class DisplayIffCondition(Condition):
    """
    Display field(s) if and only if the conditions in `tests` are all True
    """
    action = 'display_iff'

    def keep_fields(self, cleaned_data):
        """
        Return ``True`` if the conditions require the fields to be displayed.
        """
        is_displayed = all(test(cleaned_data) for test in self.tests)
        return is_displayed

    def __repr__(self):
        return "<Condition {name}: Display {fields} if {tests}>".format(
            fields=self.fields_ids,
            tests=self.tests,
            name=self.name)
