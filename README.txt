.. contents::

Introduction
============

This recipe installs Celery and creates a ``celeryconfig.py`` module with
the specified configuration options. It helps managing multiple configurations
(e.g. development and production) using buildout.

You can use it in a part like this::

    [celery]
    recipe = collective.recipe.celery
    broker-transport = sqlakombu.transport.Transport
    broker-host = sqlite:///celery_broker.db
    result-backend = database
    result-dburi = sqlite:///celery_results.db
    imports = myapp.tasks
    eggs =
        kombu-sqlalchemy
        myapp

Supported options
=================

General options
---------------

eggs
    A list of additional eggs you want to make available to Celery. Use this to
    add additional dependencies such as ``kombu-sqlalchemy`` or the module(s)
    containing your task definitions.

scripts
    Controls which scripts are generated. If the option is omitted, then all
    scripts will be generated. If no value is given, then script generation is
    disabled.

config-path
    The location of the directory containing the ``celeryconfig.py`` module. By
    default the config module is created in the part directory.
    You can use this in other parts to include the config module::

        [celery]
        recipe = collective.recipe.celery

        [myapp]
        recipe = zc.recipe.egg
        eggs = myapp
        extra-paths = ${celery:config-path}

Celery options
--------------

The following configuration options are supported. See Celery documentation for
more details.

broker-transport
    The Kombu transport to use. You can use a custom transport class name, or
    select one of the built-in transports: ``amqplib``, ``pika``, ``redis``, 
    ``beanstalk``, ``sqlalchemy``, ``django``, ``mongodb``, ``couchdb``.

broker-host
    The hostname of the broker.

broker-port
    The port number of the broker.

broker-user
    The username to connect as.

broker-password
    The password to connect with.

broker-vhost
    The virtual host.

result-backend
    The backend used to store task results. Can be one of ``database``,
    ``cache``, ``mongodb``, ``redis``, ``tyrant`` or ``amqp``.

result-dburi
    Connection string for the database result backend.

imports
    A list of modules to import when the celery daemon starts. Specify one
    module per line.

celeryd-log-file
    The filename where the celery daemon logs messages to.

celeryd-log-level
    The log level, can be one of ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR`` or
    ``CRITICAL``.

celeryd-concurrency
    The number of concurrent worker processes/threads/green threads, executing
    tasks.

additional-config
    Any additional configuration directives can be added using the
    ``additional-config`` option.
    
    Example::
    
        additional-config =
            CELERY_TASK_PUBLISH_RETRY=True
            CELERY_TASK_PUBLISH_RETRY_POLICY={"max_retries": 2,
                                              "interval_start": 10,
                                              "interval_step": 0,
                                              "interval_max": 10}
