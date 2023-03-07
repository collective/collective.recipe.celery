"""Mapping of recipe options to celery configuration directives.
"""

STRING_OPTIONS = {
    'broker-url': 'broker_url',
    'broker-password': 'redis_password',
    'broker-transport': 'broker_transport',
    'broker-user': 'redis_username',
    'result-backend': 'result_backend',
    'broker-host': 'broker_host',
}

NUMERIC_OPTIONS = {
    'broker-port': 'broker_port',
    'celeryd-concurrency': 'worker_concurrency',
}

SEQUENCE_OPTIONS = {
    'imports': 'imports',
}
