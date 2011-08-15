Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = celery
    ... index = %(server)s/index
    ... find-links = %(server)s
    ... 
    ... [celery]
    ... recipe = collective.recipe.celery
    ... broker-transport = sqlakombu.transport.Transport
    ... broker-host = sqlite:///celery_broker.db
    ... result-backend = database
    ... result-dburi = sqlite:///celery_results.db
    ... imports = myapp.tasks
    ... """% dict(server=link_server))

Running the buildout gives us::

    >>> print system(buildout)
    Installing celery.
    celery: Creating directory /sample-buildout/parts/celery.
    celery: Generated config file /sample-buildout/parts/celery/celeryconfig.py.
    Getting distribution for 'celery'.
    Got celery 2.3.1.
    Generated script '/sample-buildout/bin/celeryctl'.
    Generated script '/sample-buildout/bin/celeryd'.
    <BLANKLINE>

Check that we have the celery scripts::

    >>> ls(sample_buildout, 'bin')
    -  buildout
    -  celeryctl
    -  celeryd

Check that we got a celery config file::

    >>> ls(sample_buildout, 'parts', 'celery')
    - celeryconfig.py

If we run the celeryd script, it prints out the config data::

    >>> print(system(join(sample_buildout, 'bin', 'celeryd')))
    BROKER_HOST='sqlite:///celery_broker.db'
    BROKER_TRANSPORT='sqlakombu.transport.Transport'
    CELERY_IMPORTS=('myapp.tasks',)
    CELERY_RESULT_BACKEND='database'
    CELERY_RESULT_DBURI='sqlite:///celery_results.db'
    <BLANKLINE>

We can include additional eggs using the eggs option::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = celery
    ... index = %(server)s/index
    ... find-links = %(server)s
    ... 
    ... [celery]
    ... recipe = collective.recipe.celery
    ... eggs =
    ...     other
    ... """% dict(server=link_server))

    >>> print system(buildout),
    Uninstalling celery.
    Installing celery.
    celery: Generated config file /sample-buildout/parts/celery/celeryconfig.py.
    Getting distribution for 'other'.
    Got other 1.0.
    Generated script '/sample-buildout/bin/celeryctl'.
    Generated script '/sample-buildout/bin/celeryd'.

We can control which scripts are generated using the scripts option.
If no value is given, then script generation is disabled::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = celery
    ... index = %(server)s/index
    ... find-links = %(server)s
    ... 
    ... [celery]
    ... recipe = collective.recipe.celery
    ... scripts =
    ... """% dict(server=link_server))

    >>> print system(buildout),
    Uninstalling celery.
    Installing celery.
    celery: Generated config file /sample-buildout/parts/celery/celeryconfig.py.

    >>> ls(sample_buildout, 'bin')
    -  buildout

Let's create the celeryd script only::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = celery
    ... index = %(server)s/index
    ... find-links = %(server)s
    ... 
    ... [celery]
    ... recipe = collective.recipe.celery
    ... scripts =
    ...     celeryd
    ... """% dict(server=link_server))

    >>> print system(buildout),
    Uninstalling celery.
    Installing celery.
    celery: Generated config file /sample-buildout/parts/celery/celeryconfig.py.
    Generated script '/sample-buildout/bin/celeryd'.

    >>> ls(sample_buildout, 'bin')
    -  buildout
    -  celeryd

The supported configuration directives may be of various types including
strings, integers and tuples::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = celery
    ... index = %(server)s/index
    ... find-links = %(server)s
    ... 
    ... [celery]
    ... recipe = collective.recipe.celery
    ... broker-port = 8080
    ... broker-user = guest
    ... imports =
    ...     myapp.tasks
    ...     other.tasks
    ... """% dict(server=link_server))

    >>> print system(buildout),
    Uninstalling celery.
    Installing celery.
    celery: Generated config file /sample-buildout/parts/celery/celeryconfig.py.
    Generated script '/sample-buildout/bin/celeryctl'.
    Generated script '/sample-buildout/bin/celeryd'.

Let's verify the generated config data::

    >>> cat(sample_buildout, 'parts', 'celery', 'celeryconfig.py')
    BROKER_PORT = 8080
    BROKER_USER = 'guest'
    CELERY_IMPORTS = ('myapp.tasks', 'other.tasks')
    <BLANKLINE>

The recipe supports a limited set of celery's configuration directives. Any
additional directives can be added using the additional-config option::

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = celery
    ... index = %(server)s/index
    ... find-links = %(server)s
    ... 
    ... [celery]
    ... recipe = collective.recipe.celery
    ... additional-config =
    ...     CELERY_TASK_PUBLISH_RETRY = True
    ...     CELERY_TASK_PUBLISH_RETRY_POLICY = {"max_retries": 2,
    ...                                         "interval_start": 10,
    ...                                         "interval_step": 0,
    ...                                         "interval_max": 10}
    ... """% dict(server=link_server))

    >>> print system(buildout),
    Uninstalling celery.
    Installing celery.
    celery: Generated config file /sample-buildout/parts/celery/celeryconfig.py.
    Generated script '/sample-buildout/bin/celeryctl'.
    Generated script '/sample-buildout/bin/celeryd'.

Let's verify the generated config data::

    >>> cat(sample_buildout, 'parts', 'celery', 'celeryconfig.py')
    CELERY_TASK_PUBLISH_RETRY = True
    CELERY_TASK_PUBLISH_RETRY_POLICY = {"max_retries": 2,
    "interval_start": 10,
    "interval_step": 0,
    "interval_max": 10}
    <BLANKLINE>
