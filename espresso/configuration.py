from configparser import ConfigParser


class Configuration(object):
    """
    Configurations
    ==============

    Configurations are going to be managed in namespaces, that is, we can 
    create a particular namespace in espresso and then look this setting
    later, but any module can use its own namespace.

    The configurations are going to be stored in the filesystem in the path:

       /etc/espresso/conf.d/<namespace>.conf

    Using the configparser module, then using ini-like configs.

    An option is specified then by namespace.section.name and is stored as
    a single string.
    
    """

    def __init__(self, namespace):
        self.namespace = namespace

    def get(self, section, name):
        " Get an option."

        conf = ConfigParser()
        conf.read('/etc/espresso/conf.d/%s.conf' % (self.namespace, ))
        return conf.get(section, name)

    def set(self, section, name, value):
        " Set an option."

        conf = ConfigParser()
        conf.read('/etc/espresso/conf.d/%s.conf' % (self.namespace, ))

        # Check for section
        if not conf.has_section(section):
            conf.add_section(section)
        
        conf.set(section, name, value)

        # Write back configurations.
        with open('/etc/espresso/conf.d/%s.conf' % (self.namespace, ), 'w') as fd:
            conf.write(fd)
