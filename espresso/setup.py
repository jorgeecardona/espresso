import os

def main():
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
    
