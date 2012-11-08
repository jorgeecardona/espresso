import argparse
from espresso.configuration import Configuration


def main(argv=None):
    """
    Basic cli for espresso.

    For now we just need to handle configurations.

    """

    # Create parser.
    parser = argparse.ArgumentParser(description="Espresso command-line interface")

    # Select the namespace used.
    parser.add_argument('--namespace', help="Select namespace for any operation.", 
                        required=True)
    
    # Add argument.
    parser.add_argument('--add-option', nargs=2, dest="add_option", default=None,
                        help="Add a new option, eg: general.ip 1.1.1.1")

    # Parse the args.
    args = parser.parse_args(argv)

    # Check if we want to add an option.
    if args.add_option is not None:

        # Get section and name.
        section, name = args.add_option[0].split('.')

        # Get value.
        value = args.add_option[2]

        # Use the namespace.
        Configuration(args.namespace).set(section, name, value)
