Espresso
========

This is a just born tool to *manage* machines from a cli and also programatically.


Goals
-----

We need to define somehow a recipe/confi/description/spec file that defines what we want. We must be able to apply this, in any async way, or as a daemon system that detect to misbehaviours and correct them, as a daemon listening for changes.

Describing a system
-------------------

We're going to use YAML as the markup language to define the system, using tags we can
define which components are existing in the platform. 

Library vs Shell
----------------

The idea is to be able to use espresso either as a library or as a command shell, then we will be able to do this:

    from espresso.barista import Barista

    b = Barista()
    b.brew('/tmp/desc.yaml')

or:

    from espress.types import File
    f = File('/tmp/somefile', content="Hello world!", owner="root", group="audio")


Also a CLI will be defined to use like:

     barista --brew /tmp/desc.yaml

Adding new types
----------------

Adding new types must be easy to do, assign them a possible tag to be encounter in a description. We must be thinking in an option to add them as plugins.

Templating
----------

Since yaml has no variables, I imagine the best option is to define a templating stage in which the files are just templates that crates a valid yaml file, then it would be impossible to use current types to feed the template.


Multiple files
--------------

How to define a standard way to combine description in several files.
