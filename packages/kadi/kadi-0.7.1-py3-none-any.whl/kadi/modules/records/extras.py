# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime
from datetime import timezone

from flask import request
from marshmallow import fields
from marshmallow import validates_schema
from marshmallow import ValidationError
from sqlalchemy.dialects.postgresql import JSONB

from kadi.ext.db import db
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.format import pretty_type_name
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import NonEmptyString
from kadi.lib.utils import is_iterable
from kadi.lib.utils import is_special_float
from kadi.lib.utils import named_tuple
from kadi.lib.utils import parse_datetime_string


MAX_INTEGER = 2 ** 53 - 1


def is_nested_type(type_value):
    """Check if the type of an extra metadata entry is nested.

    :param type_value: The type of the extra metadata entry.
    :return: ``True`` if the given type is nested, ``False`` otherwise.
    """
    return type_value in ["dict", "list"]


class ExtrasJSONB(db.TypeDecorator):
    """Custom JSON type for values containing extra record metadata.

    Converts float values to float explicitely, as very large float values would
    otherwise be interpreted as integers. This also works with dictionaries that do not
    contain extras directly, but as any nested dictionary value instead. See also
    :attr:`.Record.extras`.
    """

    impl = JSONB

    def _is_extra(self, value):
        # Extras always include a type and value, so this should be good enough to
        # detect them.
        if isinstance(value, dict) and "type" in value and "value" in value:
            return True

        return False

    def process_result_value(self, value, dialect):
        """Convert float values of any extras recursively."""
        if value is None:
            return value

        if isinstance(value, dict):
            for _, val in value.items():
                self.process_result_value(val, dialect)

        elif isinstance(value, list) and len(value) > 0 and self._is_extra(value[0]):
            for extra in value:
                if is_nested_type(extra["type"]):
                    self.process_result_value(extra["value"], dialect)

                elif extra["type"] == "float" and extra["value"]:
                    extra["value"] = float(extra["value"])

        return value


class ExtraSchema(KadiSchema):
    """Schema to represent extra record metadata.

    When deserializing, also does all necessary conversion and validation. See also
    :attr:`.Record.extras`.
    """

    key = NonEmptyString(required=True, filters=[normalize])

    value = fields.Raw(missing=None)

    unit = NonEmptyString(missing=None, filters=[normalize])

    type = NonEmptyString(required=True, filters=[strip])

    @staticmethod
    def _add_validation_error(errors, index, field, message):
        if index not in errors:
            errors[index] = {field: [message]}
        elif field not in errors[index]:
            errors[index][field] = [message]
        else:
            errors[index][field].append(message)

    @validates_schema(pass_many=True, skip_on_field_errors=False)
    def _validates_schema(self, data, many, **kwargs):
        data = data if many else [data]
        validation_errors = {}
        prev_keys = set()

        for index, extra in enumerate(data):
            key = extra.get("key")
            value = extra.get("value")
            unit = extra.get("unit")
            type_value = extra.get("type")

            if isinstance(value, str):
                value = value.strip()
                if not value:
                    value = None

                extra["value"] = value

            if type_value not in ["int", "float"]:
                if unit is not None:
                    self._add_validation_error(
                        validation_errors,
                        index,
                        "unit",
                        f"Cannot be used together with {type_value}.",
                    )

                # If no unit can be given it should not be included in the output at
                # all.
                if "unit" in extra:
                    del extra["unit"]

            if key in prev_keys:
                self._add_validation_error(
                    validation_errors, index, "key", "Duplicate value."
                )

            if type_value not in [
                "str",
                "int",
                "float",
                "bool",
                "date",
                "dict",
                "list",
            ]:
                self._add_validation_error(
                    validation_errors, index, "type", "Invalid value."
                )
            else:
                if is_nested_type(type_value):
                    if type_value == "list":
                        # List values should have no keys at all.
                        schema = ExtraSchema(many=True, exclude=["key"])
                    else:
                        schema = ExtraSchema(many=True)

                    try:
                        # Parse nested values recursively.
                        extra["value"] = schema.load(value)
                    except ValidationError as e:
                        messages = e.messages
                        # The index of the current error will not be included
                        # otherwise.
                        if not is_iterable(value):
                            messages = {0: messages}

                        validation_errors[index] = {"value": messages}

                elif value is not None:
                    validation_error = False

                    if type_value == "int":
                        # Restrict integer values to values safe for parsing them in JS
                        # contexts for now, as they are also used for the extra metadata
                        # editor. This is not quite the whole long integer range, but
                        # hopefully enough for most use cases. As a positive side
                        # effect, all integer values are indexable by Elasticsearch.
                        if type(value).__name__ != type_value or value > MAX_INTEGER:
                            validation_error = True

                    elif type_value == "float":
                        # Allow integer values as well.
                        if type(value).__name__ in ["int", "float"]:
                            value = float(value)

                            # Do not allow special float values.
                            if is_special_float(value):
                                validation_error = True

                            extra["value"] = value
                        else:
                            validation_error = True

                    elif type_value == "date":
                        # Also allow using datetime objects directly.
                        if not isinstance(value, datetime):
                            value = parse_datetime_string(value)

                        if value is not None:
                            extra["value"] = value.astimezone(timezone.utc).isoformat()
                        else:
                            validation_error = True

                    elif type(value).__name__ != type_value:
                        validation_error = True

                    if validation_error:
                        self._add_validation_error(
                            validation_errors,
                            index,
                            "value",
                            f"Not a valid {type_value}.",
                        )

            if key:
                prev_keys.add(key)

        if validation_errors:
            raise ValidationError(validation_errors)


def _str_to_value(string, type_value):
    if string == "":
        return None

    if type_value == "int":
        value = int(string)
        # See the comment in the schema validation function above for more information.
        if value > MAX_INTEGER:
            raise ValueError

        return value

    if type_value == "float":
        value = float(string)
        # Do not allow special float values.
        if is_special_float(value):
            raise ValueError

        return value

    if type_value == "bool":
        if string == "true":
            return True
        if string == "false":
            return False

        raise ValueError

    if type_value == "date":
        value = parse_datetime_string(string)

        if value is not None:
            return value.isoformat()

        raise ValueError

    return string


def _formdata_to_extras(formdata):
    extras = []

    for parsed_extra in formdata:
        key = parsed_extra["key"]["value"]
        value = parsed_extra["value"]["value"]
        unit = parsed_extra["unit"]["value"]
        type_value = parsed_extra["type"]["value"]

        extra = {"key": key or None, "unit": unit or None, "type": type_value}

        if not extra["key"]:
            del extra["key"]

        if type_value not in ["int", "float"]:
            del extra["unit"]

        if is_nested_type(type_value):
            value = _formdata_to_extras(value)
        else:
            value = _str_to_value(value, type_value)

        extra["value"] = value
        extras.append(extra)

    return extras


def _parse_formdata(formdata, is_valid=True, inside_list=False, current_depth=0):
    prev_keys = set()
    extra_formdata = []

    while formdata:
        item = formdata.pop(0)
        key, value, unit, type_value, depth = item

        try:
            depth = int(depth)
        except ValueError:
            continue

        # Check if we stepped outside the current nested value.
        if depth < current_depth:
            # Put the item back so we can process it again.
            formdata.insert(0, item)
            break

        key = normalize(key.strip())
        key = key if not inside_list else ""

        unit = normalize(unit.strip())
        unit = unit if type_value in ["int", "float"] else ""

        value = value.strip()

        extra = {
            "key": {"value": key, "errors": []},
            "value": {"value": value, "errors": []},
            "unit": {"value": unit, "errors": []},
            "type": {"value": type_value, "errors": []},
        }

        # Empty extras are skipped, except for nested values and all values inside
        # lists.
        if not key and not value and not is_nested_type(type_value) and not inside_list:
            continue

        # Extras with a value but no key are invalid, including nested values, but not
        # values inside lists.
        if not key and (value or is_nested_type(type_value)) and not inside_list:
            extra["key"]["errors"].append("Missing value.")
            is_valid = False

        if key in prev_keys:
            extra["key"]["errors"].append("Duplicate value.")
            is_valid = False

        if type_value not in ["str", "int", "float", "bool", "date", "dict", "list"]:
            extra["type"]["value"] = "str"
            extra["type"]["errors"].append("Invalid value.")
            is_valid = False

        else:
            if is_nested_type(type_value):
                # Parse nested values recursively.
                is_valid, extra["value"]["value"] = _parse_formdata(
                    formdata,
                    is_valid=is_valid,
                    inside_list=type_value == "list",
                    current_depth=depth + 1,
                )
            else:
                try:
                    _str_to_value(value, type_value)
                except ValueError:
                    extra["value"]["errors"].append(
                        f"Not a valid {pretty_type_name(type_value)}."
                    )
                    is_valid = False

                    # All other values should be kept since maybe it was just the type
                    # that was wrongly selected.
                    if type_value in ["bool", "date"]:
                        value = ""

                    extra["value"]["value"] = value

        if key:
            prev_keys.add(key)

        extra_formdata.append(extra)

    return is_valid, extra_formdata


def parse_extra_formdata(formdata=None):
    """Parse form data of extra record metadata.

    Form data needs some special handling, mainly since everything is a string. For
    general validation of extras, :class:`ExtraSchema` is more suitable. See also
    :attr:`.Record.extras`.

    :param formdata: (optional) The form data to parse as a werkzeug ``MultiDict``.
        Defaults to the form data of the current request.
    :return: An object with the following attributes:

        * **is_valid**: ``True`` if the extras are valid, ``False`` otherwise.
        * **values**: The parsed extras if ``is_valid`` is ``True``, ``None`` otherwise.
        * **formdata**: A list of validated (and possibly converted) formdata in the
          following form:

            .. code-block:: python3

                [
                    {
                        "key": {"value": "foo", "errors": []},
                        "value": {"value": "1", "errors": []},
                        "unit": {"value": "", "errors": []},
                        "type": {"value": "int", "errors": []},
                    }
                ]
    """
    form = formdata if formdata is not None else request.form

    formdata = zip(
        form.getlist("extra_key"),
        form.getlist("extra_value"),
        form.getlist("extra_unit"),
        form.getlist("extra_type"),
        form.getlist("extra_depth"),
    )

    is_valid, formdata = _parse_formdata(list(formdata))

    extras = None
    if is_valid:
        extras = _formdata_to_extras(formdata)

    return named_tuple("Extras", is_valid=is_valid, formdata=formdata, values=extras)
