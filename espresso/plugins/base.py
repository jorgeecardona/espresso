


class EspressoPlugin(object):
    """    
    Espresso plugin
    ===============
    
    """            

    def define(self, component):
        " Define a component."

        # Get the inner type of component.
        type = component.type.replace('-', '_').split('.', 1)[-1]

        # Get method.
        method = getattr(self, 'define_%s' % (type, ))

        # Run method.
        method(component)

    
