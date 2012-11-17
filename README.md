========
Espresso
========

[![Build Status](https://travis-ci.org/jorgeecardona/espresso.png)](https://travis-ci.org/jorgeecardona/espresso)


The goal of Espresso is to help in the management of configuration and integration of services in different servers.

For now is just defining stages and some helpers to work with shell, dpkg, fstab and file system.

Current State
=============

Stages
------

Stages are just a way to combine different aspects of your configuration, like: setup the repositories, or 'create the directory structure', 'ensure needed libraries'.

Between stages can be defined some control flow, as requires control. 

In a future also signal will be available between stages.

Example:

    from espresso.stage import Stage
    from espresso.helpers import fs, dpkg

    class SetupRepositoryStage(Stage):
        """
	Setup Repository
 	================

	This stage will define the esential aspects of the repositories in the
	system.

	Look how nice is to have docs in the configuration, you can explain a lot
	of things in here, as rationale for decisions and you can read this in a 
	couple of months and will understand immediately.

	"""

        class Meta:
	    name = 'setup-repository'
	    
        def run(self, storage=Storage()):

	    # Directory storage of useful files.
	    storage = DirectoryStorage('/tmp')

	    # Ensure the content of the sources.            
            fs.ensure_file('/etc/apt/sources.list', content=storage['sources.list'])
	    dpkg.update()	    					 
	    
    class MainStage(Stage):
        """
	Main
	====

	Our main system is based just in two packages, pretty silly but that's 
	how it is.

	"""

        class Meta:
            name = 'main'
            requires = SetupRepositoryStage()

        def run(self):

	    # We just need two packages.
            dpkg.ensure_installed('portsentry', 'python2.7')


    if __name__ == '__main__':

        stage = MainStage()

	# This will run also the run for SetupRepositoryStage thanks to
	# the Stage's metaclass.

        stage.run()


We can also run this from the console with (with the above in stages.py):

    espresso -S stages --run=main


File's Storage
--------------

There is a basic storage defined in `espresso.storage` to get files from a set of directories. 

Currently just directory storage, and http storage and cloudfiles on its way (more likely with libcloud).

Configurations
--------------

A set of global configurations can be set separated in namespaces to be used from any stage of the configuration.


Future Ideas
============

 - Components (helpers??).
 - Signals between stages.