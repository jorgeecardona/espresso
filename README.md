========
Espresso
========

The goal of Espresso is to help in the management of configuration and integration of services in different servers.

For now is just a wrapper to configurations using namespaces.

Future Ideas
============

 - Components.


What do we need to manage servers?
----------------------------------

These are some of the componentes needed in order to manage a big infrastructure.

- Messaging system between servers


Some messaging system close to AMQP but lighter would be really nice to have, ZeroMQ seems to be the perfect tool to do it, also some kind of distributed queue based on
quourum systems and taking the main ideas of AMQP.

- Plugins in top of the messages

Basically after the messaging system a set of plugable tool that catch this messages would be great to manage the server in different ways.

- Goals

1) Be able to use this in a single server.

2) No single points of failure, no master-slave configurations, all the servers are equal up to some tagging and classification between them, but there is not holy master server.

3) A good set of native plugins to set up basic things in the server, and to run tasks, and a global cron system.

