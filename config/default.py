import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@localhost:5432/dkmh"
ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = 'FF97FADD11E6A454D89918E7C6B907284ACEC3EE3D63A3E9D40A02537349BB1DE37ACAA2C695E16D0C03BD5A41A3E5AD19EECA01AF80C832A359D2D55F144B13D8F57D3CD006C40C402509D6C8FFA6435B9DD017C0F6449B6486ECAAC7EB3D0C48DBB807D22578C29D8B91B0A82860F5B28D5DB818665886E7A37FCAA45FC8C8'

class DefaultConfig(object):
    """Flask configuration."""

    TESTING = True
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'GDtfDCFYjD'

class PgConnection:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def conn_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    