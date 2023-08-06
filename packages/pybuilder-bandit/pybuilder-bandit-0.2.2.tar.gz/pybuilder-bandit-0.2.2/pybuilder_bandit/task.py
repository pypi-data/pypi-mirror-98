#   -*- coding: utf-8 -*-
import re
import json
from string import Template
from pybuilder.core import init
from pybuilder.core import task
from pybuilder.core import depends
from pybuilder.errors import BuildFailedException
from pybuilder.pluginhelper.external_command import ExternalCommandBuilder
from pybuilder.plugins.python.python_plugin_helper import log_report

SUMMARY = Template("""
    Test results:
        Number of issues identified: ${total}
    Code scanned:
        Total lines of code: ${loc}
        Total lines skipped (#nosec): ${nosec}
    Run metrics:
        Total issues (by severity):
            Undefined: ${severity_undefined}
            Low: ${severity_low}
            Medium: ${severity_medium}
            High: ${severity_high}
        Total issues (by confidence):
            Undefined: ${confidence_undefined}
            Low: ${confidence_low}
            Medium: ${confidence_medium}
            High: ${confidence_high}""")


@init
def init_bandit(project):
    """ initialize complexity task properties
    """
    project.plugin_depends_on('bandit')
    project.set_property_if_unset('bandit_break_build', False)
    project.set_property_if_unset('bandit_confidence_level', 'LOW')
    project.set_property_if_unset('bandit_severity_level', 'LOW')
    project.set_property_if_unset('bandit_skip_ids', None)
    project.set_property_if_unset('bandit_include_testsources', False)
    project.set_property_if_unset('bandit_include_scripts', False)


@task('bandit', description='execute bandit security linter')
@depends('prepare')
def bandit(project, logger, reactor):
    """ execute bandit security linter
    """
    output_filename = project.expand_path('$dir_reports', 'bandit.json')
    include_test_sources = project.get_property('bandit_include_testsources')
    include_scripts = project.get_property('bandit_include_scripts')
    command = get_command(project, reactor, output_filename)
    result = command.run_on_production_source_files(
        logger,
        include_dirs_only=True,
        include_test_sources=True if include_test_sources else False,
        include_scripts=True if include_scripts else False)
    process_result(project, result, logger, output_filename)


def get_command(project, reactor, output_filename):
    """ return bandit command
    """
    command = ExternalCommandBuilder('bandit', project, reactor)
    command.use_argument('--recursive')
    command.use_argument('--format')
    command.use_argument('json')
    command.use_argument('--output')
    command.use_argument(output_filename)
    command.use_argument(translate_confidence_level(project.get_property('bandit_confidence_level')))
    command.use_argument(translate_severity_level(project.get_property('bandit_severity_level')))
    skips = project.get_property('bandit_skip_ids')
    if skips:
        command.use_argument('--skip')
        command.use_argument(skips)
    return command


def translate_confidence_level(level):
    """ return confidence level
    """
    if level is None or level == 'LOW':
        return '-i'
    if level == 'MEDIUM':
        return '-ii'
    if level == 'HIGH':
        return '-iii'
    raise ValueError(f'{level} is not a valid confidence level')


def translate_severity_level(level):
    """ return severity level
    """
    if level is None or level == 'LOW':
        return '-l'
    if level == 'MEDIUM':
        return '-ll'
    if level == 'HIGH':
        return '-lll'
    raise ValueError(f'{level} is not a valid severity level')


def read_data(filename):
    """ return dictionary read from bandit json file
    """
    with open(filename) as infile:
        return json.load(infile)


def get_summary_lines(data):
    """ return string summary from bandit data
    """
    metrics = data.get('metrics', {}).get('_totals', {})
    # sanitize metrics keys to be valid variables to enable string substitution
    metrics_vars = {
        'total': len(data.get('results', []))
    }
    for key, value in metrics.items():
        metrics_vars[key.lower().replace('.', '_')] = value
    summary = SUMMARY.substitute(metrics_vars)
    # remove leading spaces from string generated from string template
    return [f'{line[4:]}\n' for line in summary.split('\n')][1:]


def process_result(project, result, logger, output_filename):
    """ process result
    """
    verbose = project.get_property('verbose')
    if verbose:
        log_report(logger, 'bandit', get_summary_lines(read_data(output_filename)))

    if result.exit_code:
        message = f'Bandit security linter detected issues, see {output_filename}'
        fail_build = project.get_property('bandit_break_build')
        if fail_build:
            raise BuildFailedException(message)
        else:
            logger.warn(message)
    else:
        logger.info('Bandit security linter found no issues')
