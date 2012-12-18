import os
import sys
import sh
import pwd
import fstab as fstab_lib
import shutil

class System(object):

    def ensure_user(self, name, home=None):
        " Ensure the presence of a user in the system and its home path."

        print(" * Check if the user exists ... ")
        
        if any(name == u.pw_name for u in pwd.getpwall()):
            print("   ... user already exists. ")
            return

        print("   ... create user ...")
        
        if home is not None:            
            sh.useradd('-d', home, '-m', name, _err=sys.stderr, _out=sys.stdout)
        else:
            sh.useradd('-m', name, _err=sys.stderr, _out=sys.stdout)
            
        print("   ... done!")


class FsTab(object):

    def remount(self, directory):
        " Remount a directory."

        sh.mount('-o', 'remount', directory, _err=sys.stderr, _out=sys.stdout)

    def ensure_option(self, option, directory):
        " Ensure an option to the mounting at a directory."

        print(" * Ensure that mount line with directory '%s' has option '%s' ..." % (
            directory, option))
        
        fs = fstab_lib.Fstab()
        fs.read('/etc/fstab')

        # Get line with file.
        line = [i for i, line in enumerate(fs.lines) if line.directory == directory]
        if len(line) == 0:
            raise ValueError("Directory is not used by any mount.")

        line = line[0]            

        # Get options.
        options = fs.lines[line].get_options()

        # Option on it?
        if option not in options:

            options.append(option)

            # Set new option.
            fs.lines[line].set_options(options)            
            
            # Write change.
            fs.write('/etc/fstab')

            print("   ... option added ...")
        
        print("   ... done!")
        

class Shell(object):
    def run(self, line):
        sh.bash('-c', line, _err=sys.stderr, _out=sys.stdout)

class DebConf(object):
    def set_selections(self, content):
        print(" * Set selections for debian packages.")
        sh.Command('debconf-set-selections')(_in=content, _err=sys.stderr, _out=sys.stdout)

class Dpkg(object):

    def add_key(self, key):
        print(" * Adding public key to repositories ...")
        sh.Command('apt-key')('add', '-', _in=key, _err=sys.stderr, _out=sys.stdout)
    
    def update(self):
        print(" * Updating dpkg repositories ...")
        sh.aptitude('-y', 'update', _err=sys.stderr, _out=sys.stdout)

    def safe_upgrade(self):
        sh.aptitude('-y', 'safe-upgrade', _err=sys.stderr, _out=sys.stdout)

    def ensure_installed(self, packages):
        sh.aptitude('-y', 'install', *packages, _err=sys.stderr, _out=sys.stdout)


class FileSystem(object):
    " Some basic functions. "

    def ensure_tree(self, path, source):
        " Copy a whole tree from a source to a destination."

        print(" * Ensuring tree at '%s' ..." % (path, ))

        # Check for source.
        if not os.path.isdir(source):
            raise TypeError("Source '%s' is not a path." % (source, ))

        # Walk thru the source.
        for orig_path, dirnames, filenames in os.walk(source):
            
            # Replace the source by the destination.
            dest_path = orig_path.replace(source, path)

            # Create destination if necessary.
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)        

            for filename in filenames:
                shutil.copyfile(os.path.join(orig_path, filename), 
                                os.path.join(dest_path, filename))
                            
        print("   ... done!")

    def ensure_file(self, path, content=None, size=None):
        " Ensure a file exists and its content."

        print(" * Ensuring that '%s' is a file ..." % (path, ))
    
        if os.path.exists(path):
            if not os.path.isfile(path):
                raise TypeError("The path is already used by a non-file.")
                
        elif size > 0:
            with open(path, 'w') as fd:                
                print("   ... ensuring size of %d bytes ..." %(size, ))
                fd.truncate(size)

        # Ensure content.
        if content is not None:
            with open(path, 'w') as fd:
                print("   ... ensuring content in the file ...")
                fd.write(content)                                        

        print("   ... done!")

    def ensure_directory(self, path, mode=None, owner=None, group=None):
        " Ensure a directory exists in a path."
        
        print(" * Ensuring that '%s' is a directory ..." % (path, ))

        if os.path.exists(path):
            if not os.path.isdir(path):
                raise TypeError("The path exists and is not a directory!")
        else:
            # Create the path.
            print("  ... creating ...")
            os.makedirs(path)
                        
        # TODO: Ensure mode, owner and group.
        print("   ... done!")


# Create helpers.
fs = FileSystem()
dpkg =Dpkg()
debconf = DebConf()
shell = Shell()
fstab = FsTab()
system = System()
