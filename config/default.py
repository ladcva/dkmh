import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
PROCESSES_FACTOR = 3 # Number of processes to run in parallel e.g. Apple M1 has 8 cores -> 8*3 = 24 processes
NUM_PROCESSES = DEFAULT_NUM_PROCESSES*PROCESSES_FACTOR
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@postgres:5432/dkmh"  # This is for Airflow DB
POSTGRES_CONN_STRING_SERVER = "postgresql+psycopg2://admin:1@localhost:5433/dkmh"

ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = "0AC540F74826F0ED760222F031A77E91F600DF9DF0572D4BDA14CBAEACDE57F1656CB19F6DBD19042A2F281B4B0713326D5DBB76CB25AC612F91538D822D02B3CC2B7B0F372BD8C1C2440BB9EF305071792E7CE46B31B57DF78E9C6C75C7F7C5B12916CDABAAE064EAC3AC015BE088D64B8EF25E612BB262E5295C5A33CE7ED0"
HP_URL = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={}&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
DKHP_URL = 'https://sv.isvnu.vn/dang-ky-hoc-phan.html'   #for worker
LH_URL = "https://sv.isvnu.vn/SinhVienDangKy/GetChiTietLichHoc" 

class DefaultConfig(object):
    """Flask configuration."""

    TESTING = True
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'GDtfDCFYjD'
    CACHE_TYPE = 'simple'

class PgConnection:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def conn_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    