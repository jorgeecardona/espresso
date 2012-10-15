import ConfigParser
import io
import sh
import time
import hashlib
import pkg_resources

from base import EspressoPlugin

class SupervisorPlugin(EspressoPlugin):

    name = 'supervisor'
    components = ['program']

    def define_program(self, component):
        " Define a program at supervisor."
        
        # Create base config
        config = ConfigParser.ConfigParser()

        main_section = 'program:%s' % (component.name, )
        
        config.add_section(main_section)

        for key in component.data:
            config.set(main_section, key, component.data[key])

        # Create an IO buffer and pass content.
        content = io.BytesIO()
        config.write(content)
        content.flush()
        content.seek(0)
        new_content = content.read()

        # Get the hash of the new content.
        content_hash = hashlib.sha1(new_content)
        
        # If content is different the change it.
        original_hash = hashlib.sha1()
        try:
            with open('/etc/supervisor/conf.d/%s.conf' % (component.name, ), 'r') as fd:
                original_hash.update(fd.read())
        except:
            pass

        if content_hash.hexdigest() != original_hash.hexdigest():
            
            # Change it.
            with open('/etc/supervisor/conf.d/%s.conf' % (component.name, ), 'w') as fd:
                fd.write(new_content)

            # Finally update supervisor.
            sh.supervisorctl('update')


supervisor = SupervisorPlugin()
