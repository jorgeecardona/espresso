import argparse
import gevent
import signal

from component import ComponentManager
from configuration import ConfigurationManager

def espresso():

    parser = argparse.ArgumentParser(description="Espresso daemon.")

    # Configuration manager.
    configuration = ConfigurationManager()
        
    # Component manager.
    components = ComponentManager(configuration)

    # Basic signal handler.
    gevent.signal(signal.SIGTERM, components.stop)
    
    # Look for components.
    components.start()
    components.join()

    
