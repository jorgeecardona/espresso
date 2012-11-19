.. Espresso documentation master file, created by
   sphinx-quickstart on Mon Nov 19 17:56:08 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Espresso's documentation!
====================================

Espresso is a tool to describe the configuration of your servers and easily manage them.

.. toctree::
   :maxdepth: 2

What is to 'Configure'?
-----------------------

Well, it sound silly but I prefer to define first what is to configure and then keep talking
about it.

Every time you deploy a server there is a work that need to be done before you can consider
is a production server.

This work is composed in different aspects: networking, security, services, integration,
et al. Some of those are pretty standard and some may be as particular as you want.

Also, some are reproducible and some are hard to reproduce in different environments.

So, roughly speaking 'to configure' is to define first the 'aspects' you need in 
your server to consider it as production ready, and the 'description' of each 
aspect.

What is 'Espresso' for?
-----------------------

Espresso is just a library that will let you to define this aspects (we call them 
stages and you can aggregate them as you want).

We have also some 'helpers' or plugins so you can reuse part of your code.

Initially the 'descriptions' are actually code, we're looking for 
the way to achive a flexible balance between mere literal descriptions and scripts
in the meantime this scripts must be 'idempotent' (you should be able to run them as many time you want, if you don't change anything in your system the result must be the same)

Some Examples
-------------


General API
-----------

= Stages

= Helpers


License
-------

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

