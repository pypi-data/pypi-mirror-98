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

from .optional_parameter import OptionalParameter
from .parameter_creation_completion import (
    complete_env,
    complete_flags,
    complete_help_text,
    complete_help_varname_from_choices,
    complete_help_varname_from_name,
    complete_help_varname_from_type,
    complete_key,
    complete_parser_from_type,
    complete_single_value_type_from_choices,
    complete_type_from_default_value
)
from .parameter_creation_validation import (
    FN_TYPE,
    ensure_choices_are_compatible_with_help_choices,
    ensure_choices_are_compatible_with_type,
    ensure_choices_are_valid,
    ensure_default_and_type_are_compatible,
    ensure_default_is_a_choice,
    ensure_default_method_has_correct_signature,
    ensure_env_is_valid,
    ensure_flags_are_valid,
    ensure_key_is_valid,
    ensure_name_is_valid,
    ensure_parser_and_serializer_are_valid,
    ensure_validations_are_valid,
    one_of,
    validate_attr_types
)


class SimpleParameter(OptionalParameter):
    def __init__(self, name, advanced=False, boot=False, choices=None, default=None, env=None, flags=None, help="",
                 help_choices=None, help_section=None, help_varname=None, key=None, parser=None,
                 secret=False, serializer=str, type=None, validation=None):
        super(SimpleParameter, self).__init__(
            name, advanced=advanced, boot=boot, default=default, env=env, flags=flags, help=help,
            help_section=help_section, help_varname=help_varname, key=key, parser=parser,
            secret=secret, serializer=serializer, type=type, validation=validation
        )
        self.choices = choices
        self.help_choices = help_choices or {}

        self.validate_attributes()
        self.complete_unspecified_attributes()
        self.validate_attributes()

    def validate_attributes(self):
        validate_attr_types(self, {
            "name": str,
            "advanced": bool,
            "boot": bool,
            "choices": one_of(list, None),
            "env": one_of(str, None),
            "flags": one_of([str], None),
            "help": str,
            "help_choices": one_of(dict, None),
            "help_section": one_of(str, None),
            "help_varname": one_of(str, None),
            "key": one_of(str, None),
            "parser": one_of(FN_TYPE, type, None),
            "secret": bool,
            "serializer": one_of(FN_TYPE, type, None),
            "type": one_of(type, None),
            "validation": one_of(FN_TYPE, [FN_TYPE], None),
        })

        ensure_name_is_valid(self)
        ensure_default_and_type_are_compatible(self)
        ensure_choices_are_valid(self)
        if callable(self.default):
            ensure_default_method_has_correct_signature(self)
        else:
            ensure_default_is_a_choice(self)
        ensure_choices_are_compatible_with_type(self)
        ensure_choices_are_compatible_with_help_choices(self)
        ensure_env_is_valid(self)
        ensure_flags_are_valid(self)
        ensure_key_is_valid(self)
        ensure_parser_and_serializer_are_valid(self)
        ensure_validations_are_valid(self)

    def complete_unspecified_attributes(self):
        complete_env(self)
        complete_flags(self)
        complete_help_text(self)
        complete_key(self)

        if self.type is None:
            complete_type_from_default_value(self)
        if self.type is None:
            complete_single_value_type_from_choices(self)
        if self.type is None:
            self.type = str

        if self.help_varname is None:
            complete_help_varname_from_type(self)
        if self.help_varname is None:
            complete_help_varname_from_choices(self)
        if self.help_varname is None:
            complete_help_varname_from_name(self)

        complete_parser_from_type(self)
