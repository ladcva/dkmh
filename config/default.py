import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8


class DefaultConfig(object):
    """Flask configuration."""

    TESTING = True
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'GDtfDCFYjD'