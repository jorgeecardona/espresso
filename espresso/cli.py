import argparse
from barista import Barista


def barista():
    " Espresso CLI."

    parser = argparse.ArgumentParser(description="Brew some coffee")

    # Add brew argument as a filename to open.
    parser.add_argument(
        '--brew', dest='brew', help='File with yaml description')

    # Parse arguments
    args = parser.parse_args()

    # Define a base barista.
    if 'brew' in args:
        b = Barista()
        b.brew(args.brew)
