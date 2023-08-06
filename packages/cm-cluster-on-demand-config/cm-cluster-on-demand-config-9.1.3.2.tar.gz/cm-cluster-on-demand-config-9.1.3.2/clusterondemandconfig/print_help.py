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

from __future__ import absolute_import, print_function

import os
import sys
import textwrap

from .parameter import (
    EnumerationParameter,
    PositionalParameter,
    RepeatingPositionalParameter,
    SimplePositionalParameter,
    SwitchParameter
)

NAME_INDENT = " " * 2
HELP_INDENT = " " * 25
INFO_INDENT = " " * 15
MAX_HELP_WIDTH = 80
MAX_USAGE_WIDTH = 100
SPACE = "  "
DEFAULT_HELP_SECTION = "other optional parameters"


def print_help(command, configuration):
    """Generate the help message for this command to stdout.

    Prints a usage line and then a list of all optional parameters grouped by their sections.
    """
    positionals, optionals = _group_parameters_by_type(command.parameters, configuration)

    _print_usage_line(command)
    _print_command_description(command)

    if positionals:
        _print_positional_parameters(positionals)
    if optionals:
        _print_optional_non_positional_parameters(optionals, command.important_help_sections, configuration)


def print_help_for_positionals_missing_required_value(command, configuration):
    """Generate the usage message for this command to stdout.

    Similar to print_help, but only prints a usage line and the missing required parameters.
    """
    missing = configuration.required_positionals_with_missing_values()

    _print_usage_line(command)

    print("error: need to specify value for: %s" % (", ".join([p.name for p in missing])))


def print_help_for_unknown_parameters(command, unknown_parameters):
    """Inform the user of the bad parameters while showing the correct usage."""
    _print_usage_line(command)

    _print_empty_line()
    print("error: unrecognized arguments: %s" % (" ".join(unknown_parameters)))


def _group_parameters_by_type(parameters, configuration):
    positionals, optionals = [], []

    for parameter in parameters:
        if isinstance(parameter, PositionalParameter):
            positionals.append(parameter)
        else:
            optionals.append(parameter)

    return (positionals, optionals)


def _print_usage_line(command):
    prog_name = os.path.basename(sys.argv[0])
    positionals = [p for p in command.parameters if isinstance(p, PositionalParameter)]

    usage = "usage: %s %s %s [options]" % (prog_name, command.group.name, command.name)
    if positionals:
        usage += " -- %s" % (_usage_for_positionals(positionals))

    print(usage)


def _print_command_description(command):
    wrapped_description = "\n".join(textwrap.wrap(
        command.help,
        MAX_HELP_WIDTH,
        initial_indent=INFO_INDENT,
        subsequent_indent=INFO_INDENT
    ))

    _print_empty_line()
    print(wrapped_description)


def _usage_for_positionals(positionals):
    singles = [p for p in positionals if isinstance(p, SimplePositionalParameter)]
    repeatings = [p for p in positionals if isinstance(p, RepeatingPositionalParameter)]

    usages = []
    usages.extend(["%s" % single.name for single in singles])
    usages.extend(["%s [%s ...]" % (repeating.name, repeating.name) for repeating in repeatings])

    return " ".join(usages)


def _print_positional_parameters(positionals):
    _print_empty_line()
    print("positional parameters:")
    for positional in positionals:
        _print_parameter(positional)


def _print_optional_non_positional_parameters(optionals, help_section_order, configuration):
    help_section_to_parameters = _group_parameters_by_help_section(optionals)

    skipped_sections = {}
    for help_section in _sort_help_sections(list(help_section_to_parameters.keys()), help_section_order):
        if _help_section_only_shown_in_advanced(help_section_to_parameters[help_section], configuration):
            skipped_sections[help_section] = help_section_to_parameters[help_section]
        else:
            _print_help_section(help_section, help_section_to_parameters[help_section], configuration)

    _print_notice_about_skipped_advanced_sections(skipped_sections)


def _print_notice_about_skipped_advanced_sections(sections):
    if not sections:
        return

    n_parameters = sum(len(parameters) for parameters in sections.values())

    print("Some sections were omitted")
    print((
        "%d sections with a total of %d parameters "
        "can be displayed with the --advanced-help argument" % (len(sections), n_parameters)
    ))


def _group_parameters_by_help_section(parameters):
    help_section_to_parameters = {}

    for parameter in parameters:
        help_section = parameter.help_section or DEFAULT_HELP_SECTION

        if help_section not in help_section_to_parameters:
            help_section_to_parameters[help_section] = []
        help_section_to_parameters[help_section].append(parameter)

    return help_section_to_parameters


def _sort_help_sections(help_sections, help_section_order):
    order_specified, other = [], []

    for help_section in help_sections:
        if help_section in help_section_order:
            order_specified.append(help_section)
        elif DEFAULT_HELP_SECTION != help_section:
            other.append(help_section)

    sorted_help_sections = sorted(order_specified, key=lambda hs: help_section_order.index(hs)) + sorted(other)
    if DEFAULT_HELP_SECTION in help_sections:
        sorted_help_sections.append(DEFAULT_HELP_SECTION)
    return sorted_help_sections


def _print_help_section(help_section, parameters, configuration):
    if not parameters:
        return

    _print_empty_line()
    print(help_section + ":")

    n_skipped_parameters = 0
    for parameter in parameters:
        if not parameter.advanced or configuration["advanced_help"]:
            _print_parameter(parameter)
        else:
            n_skipped_parameters += 1

        modifiers = _parameter_modifiers(parameter)
        if configuration["advanced_help"]:
            for (usage, help_text) in modifiers:
                _print_parameter_usage_and_help_text(usage=usage, help_text=help_text)
        else:
            n_skipped_parameters += len(modifiers)

    if not configuration["advanced_help"] and n_skipped_parameters > 0:
        _print_number_of_skipped_parameters(n_skipped_parameters)
    _print_empty_line()


def _help_section_only_shown_in_advanced(parameters, configuration):
    only_advanced_parameters = all([p.advanced for p in parameters])
    return only_advanced_parameters and not configuration["advanced_help"]


def _print_parameter(parameter):
    help_text = parameter.help
    if hasattr(parameter, "help_choices") and parameter.help_choices:
        fragments = ["%s - %s." % (key, value) for (key, value) in parameter.help_choices.items()]
        help_text += " " + " ".join(fragments)

    _print_parameter_usage_and_help_text(
        usage=_parameter_usage(parameter),
        help_text=help_text,
    )


def _parameter_usage(parameter):
    if isinstance(parameter, PositionalParameter):
        return parameter.name
    elif isinstance(parameter, SwitchParameter):
        return ", ".join(sorted(parameter.all_flags, key=len))
    else:
        return ", ".join(["%s %s" % (flag, parameter.help_varname) for flag in sorted(parameter.all_flags, key=len)])


def _parameter_modifiers(parameter):
    if isinstance(parameter, SwitchParameter):
        return [
            (parameter.flag_with_prefix("no"),
             "To disable the switch, if previously enabled.")
        ]
    elif isinstance(parameter, EnumerationParameter):
        return [
            ("%s %s" % (parameter.flag_with_prefix("prepend"), parameter.help_varname),
             "Prepend to the existing value instead of overriding it."),
            ("%s %s" % (parameter.flag_with_prefix("append"), parameter.help_varname),
             "Append to the existing value instead of overriding it.")
        ]
    else:
        return []


def _print_parameter_usage_and_help_text(usage, help_text):
    usage = "\n".join(textwrap.wrap(usage, MAX_USAGE_WIDTH, subsequent_indent=HELP_INDENT))
    help_lines = textwrap.wrap(help_text, MAX_HELP_WIDTH, initial_indent=HELP_INDENT, subsequent_indent=HELP_INDENT)

    if len(HELP_INDENT) > len(NAME_INDENT + usage + SPACE):
        print(NAME_INDENT + usage + help_lines[0][len(NAME_INDENT + usage):])

        if len(help_lines) > 1:
            print("\n".join(help_lines[1:]))
    else:
        print(NAME_INDENT + usage)
        print("\n".join(help_lines))


def _print_number_of_skipped_parameters(n_skipped_parameters):
    print(INFO_INDENT + "(%d additional parameters can be displayed with the --advanced-help argument)" %
          (n_skipped_parameters))


def _print_empty_line():
    print("")
