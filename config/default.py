import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@postgres:5432/dkmh"  # This is for Airflow DB
POSTGRES_CONN_STRING_SERVER = "postgresql+psycopg2://admin:1@localhost:5433/dkmh"

ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = "C9F0284619E64F22681BB3542AE4140AC65A0F80E380E217DCEDC7A60CC2AEFFC3D3351F1EA886AEF59AEBC7CF6E3AA46E7B4F6C56613ABB64F963A52D8FED34C9999D50C7DC2AE20F9BA7DC426A074D9507C9EDA8101F48DBC63C04B17994576C9820E187B6BB75DC5E9D789243F1EC7C37A2F4D0ECE4DBBF631F863F4F2D0B"
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
    