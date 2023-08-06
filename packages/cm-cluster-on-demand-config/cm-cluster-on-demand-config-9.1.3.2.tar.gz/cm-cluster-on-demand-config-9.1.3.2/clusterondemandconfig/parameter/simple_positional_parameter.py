# Copyright 2004-2021 Bright Computing Holding BV
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

from .parameter_creation_completion import (
    complete_help_text,
    complete_help_varname_from_name,
    complete_key,
    complete_parser_from_type,
    complete_type_from_default_value
)
from .parameter_creation_validation import (
    FN_TYPE,
    ensure_default_and_type_are_compatible,
    ensure_default_method_has_correct_signature,
    ensure_key_is_valid,
    ensure_name_is_valid,
    ensure_parser_and_serializer_are_valid,
    ensure_validations_are_valid,
    one_of,
    validate_attr_types
)
from .positional_parameter import PositionalParameter


class SimplePositionalParameter(PositionalParameter):
    """A parameter than can only be specified on the CLI, so does not have env or flags."""

    def __init__(self, name, default=None, help="", help_section=None, help_varname=None, key=None,
                 parser=None, require_value=False, secret=False, serializer=str, type=None, validation=None):
        super(SimplePositionalParameter, self).__init__(
            name, default=default, help=help, help_section=help_section, help_varname=help_varname,
            key=key, parser=parser, require_value=require_value, secret=secret, serializer=serializer, type=type,
            validation=validation
        )
        self.validate_attributes()
        self.complete_unspecified_attributes()
        self.validate_attributes()

    def validate_attributes(self):
        validate_attr_types(self, {
            "name": str,
            "help": str,
            "help_section": one_of(str, None),
            "help_varname": one_of(str, None),
            "key": one_of(str, None),
            "parser": one_of(FN_TYPE, type, None),
            "require_value": bool,
            "serializer": one_of(FN_TYPE, type, None),
            "type": one_of(type, None),
            "validation": one_of(FN_TYPE, [FN_TYPE], None),
        })

        ensure_name_is_valid(self)
        ensure_default_and_type_are_compatible(self)
        if callable(self.default):
            ensure_default_method_has_correct_signature(self)
        ensure_key_is_valid(self)
        ensure_parser_and_serializer_are_valid(self)
        ensure_validations_are_valid(self)

    def complete_unspecified_attributes(self):
        complete_help_text(self)
        complete_key(self)
        complete_help_varname_from_name(self)

        complete_type_from_default_value(self)
        if self.type is None:
            self.type = str

        complete_parser_from_type(self)
