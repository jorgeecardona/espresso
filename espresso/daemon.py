import ConfigParser
import io
import sh
import argparse
import time
import hashlib

class Main(object):

    def run(self):

        import pkg_resources
        
        while True:
            
            reload(pkg_resources)

            for entry_point in pkg_resources.iter_entry_points('espresso.supervisor_program'):

                # Get name and data:
                data = entry_point.load()

                # Add new program.
                self.add_new_program(entry_point.name, data)
                
            time.sleep(5)

    def add_new_program(self, name, data):

        # Create base config
        config = ConfigParser.ConfigParser()

        main_section = 'program:%s' % (name, )
        
        config.add_section(main_section)

        for key in data:
            config.set(main_section, key, data[key])

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
            with open('/etc/supervisor/conf.d/%s.conf' % (name, ), 'r') as fd:
                original_hash.update(fd.read())
        except:
            pass

        if content_hash.hexdigest() != original_hash.hexdigest():
            
            # Change it.
            with open('/etc/supervisor/conf.d/%s.conf' % (name, ), 'w') as fd:
                fd.write(new_content)

            # Finally update supervisor.
            sh.supervisorctl('update')
                

def espresso():

    parser = argparse.ArgumentParser(description="Espresso daemon.")

    m = Main()
    m.run()
