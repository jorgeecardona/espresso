import pkg_resources
import time
import gevent
import logging

class ComponentManager(gevent.Greenlet):

    components = {}
    component_types = {}
    keep_running = True

    def __init__(self, configuration):
        super(ComponentManager, self).__init__()

        # Save configuration.
        self.configuration = configuration

        # Logger.
        self.logger = logging.getLogger('espresso')
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel('INFO')

    def stop(self):
        self.logger.info(" * Stop signal received, wait until next cycle to stop...")
        self.keep_running = False
        
    def _run(self):
        " Continuously look for new components."

        self.logger.info(" * Starting components manager ...")
        
        while self.keep_running:

            # Discover new types.
            self.discover_types()

            # Discover components.
            components = self.collect_components()

            # For now always try to define the component.
            for component in components:
                self.define_component(component)

            # Sleep for a while
            try:
                gevent.sleep(10)
            except KeyboardInterrupt:
                break

        self.logger.info(" * Stopping components manager.")
            
    def define_component(self, component):
        " Define a component according to its definition." 

        if component.type in self.component_types:
           
            plugin = self.component_types[component.type]

            # Use the plugin to control this component.
            plugin.define(component)

        else:
            self.logger.error("No plugin for component type: %s" % (component.type, ))

    def collect_components(self):

        import pkg_resources
        
        pkg_resources = reload(pkg_resources)

        components = []
        
        for entry_point in pkg_resources.iter_entry_points('espresso.components'):

            # Load component.
            component = entry_point.load()
            
            # We need a little match between entry_point name and component name.
            if entry_point.name == component.name:
                components.append(component)

        return components
        
                
    def discover_types(self):
        " Discover the different types of component we can handle in this system."

        import pkg_resources

        pkg_resources = reload(pkg_resources)

        for entry_point in pkg_resources.iter_entry_points('espresso.plugins'):

            print entry_point
            
            # Load plugin.
            plugin = entry_point.load()

            # Get component names that handle.
            for component in plugin.components:

                tag = '%s.%s' % (plugin.name, component)
                
                # Register this type.
                self.component_types[tag] = plugin                

    def detect_components(self):
        " Walk thru the entry_points looking for components."

        pkg_resources = reload(pkg_resources)

        # List of components.
        components = []
        
        for entry_point in pkg_resources.iter_entry_points('espresso.components'):

            # Load component.
            component = entry_point.load()

            # Validate component.
            #####

            # Add to list if valid.
            components.append(component)

        # Apply components.
        for component in components:
            if component.type in self.components:
                self.components[component.type].apply_component(component)        

class Component(object):

    def __init__(self, type, name=None, data={}):
        " Defines a new expected component in the system."

        # Component type, name and data.
        self.type = type
        self.name = name
        self.data = data        
