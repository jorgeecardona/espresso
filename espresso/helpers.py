import os
import sys
import sh
import fstab

class FsTab(object):

    def remount(self, directory):
        " Remount a directory."

        sh.mount('-o', 'remount', directory, _err=sys.stderr, _out=sys.stdout)

    def ensure_option(self, option, directory):
        " Ensure an option to the mounting at a directory."

        print(" * Ensure that mount line with directory '%s' has option '%s' ..." % (
            directory, option))
        
        fs = fstab.Fstab()
        fs.read('/etc/fstab')

        # Get line with file.
        line = [i for i, line in enumerate(fs.lines) if line.directory == directory]
        if len(line) == 0:
            raise ValueError("Directory is not used by any mount.")

        line = line[0]            

        # Option on it?
        if option not in fs.lines[line].options:

            # Set new option.
            fs.lines[line].options.append(option)
            
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
        sh.Command('debconf-set-selectios')(_in=content, _err=sys.stderr, _out=sys.stdout)

class Dpkg(object):

    def add_key(self, key):
        print(" * Adding public key to repositories ...")
        sh.Command('apt-key')('add', '-', _in=key, _err=sys.stderr, _out=sys.stdout)
    
    def update(self):
        print(" * Updating dpkg repositories ...")
        sh.aptitude('-y', 'update', _err=sys.stderr, _out=sys.stdout)

    def safe_upgrade(self):
        sh.aptitude('-y', 'safe-upgrade', _err=sys.stderr, _out=sys.stdout)

    def ensure_installed(self):
        sh.aptitude('-y', 'install', *packages, _err=sys.stderr, _out=sys.stdout)


class FileSystem(object):
    " Some basic functions. "

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