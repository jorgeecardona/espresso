import os
import sys
import argparse
import importlib

from espresso.configuration import Configuration
from espresso.stage import StageType


def setup():
    """ 
    This function must create the minimum os needs to use 
    espresso. It needs root access.

    We basically create a directory at /etc/espresso and create there
    some others like conf.d and more.
    """

    # Check that we have root access.
    if not os.geteuid() == 0:
        sys.exit("This script must be run by root.")

    # Create main path for configurations.
    os.mkdir('/etc/espresso')
    os.mkdir('/etc/espresso/conf.d')

def main_options(args):
    " Handle options subparser."

    # Check if we want to add an option.
    if args.add_option is not None:

        # Get section and name.
        section, name = args.add_option[0].split('.')

        # Get value.
        value = args.add_option[1]

        # Use the namespace.
        Configuration(args.namespace).set(section, name, value)


def main_stagging(args):
    " Handle stagging subparser."

    # We need to load some stages.
    stages_module = importlib.import_module(args.stages)

    # Real stages.
    stages = {}
    for name in stages_module.__dict__:

        # Check if its a stage.
        if not isinstance(stages_module.__dict__[name], StageType):
            continue

        # Add stage by name
        stage = stages_module.__dict__[name]

        # We can't do anything without a name.
        if 'name' not in stage._meta:
            continue

        stages[stage._meta['name']] = stage

    # Check that all the stages exists.
    for stage in args.run:
        if stage not in stages:
            raise SystemError("Non existing stage: '%s'" % (stage, ))

    # Run stages.
    for stage in args.run:
        stages[stage]().run()


def main(argv=None):
    """
    Basic cli for espresso.

    For now we just need to handle configurations.

    """

    # Create parser.
    parser = argparse.ArgumentParser(description="Espresso command-line interface")

    # Create subparser for stagging and for options
    subparsers = parser.add_subparsers(help='Espresso options and stagging commands.')

    options = subparsers.add_parser('options', help="Manage the options for later usage")
    stagging = subparsers.add_parser('stagging', help="Control stagging.")

    # Configure options parser.
    # Select the namespace used.
    options.add_argument('--namespace', help="Select namespace for any operation.", 
                         required=True)
    
    # Add argument.
    options.add_argument('--add-option', nargs=2, dest="add_option", default=None,
                         help="Add a new option, eg: general.ip 1.1.1.1")

    # Load stages.
    stagging.add_argument(
        '-S', '--stages', dest='stages', 
        help="Importable module with the stages", required=True)
    
    stagging.add_argument('-R', '--run', action='append', help="Run this stage")

    # Handlers.
    options.set_defaults(func=main_options)
    stagging.set_defaults(func=main_stagging)

    # Parse the args.
    args = parser.parse_args(argv)

    # Handle arguments
    args.func(args)
