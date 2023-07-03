import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@postgres:5432/dkmh"  # This is for Airflow DB
POSTGRES_CONN_STRING_SERVER = "postgresql+psycopg2://admin:1@localhost:5433/dkmh"

ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = "79A55C3721783DDCA5B3AF86C4263BDA6D45D8E179A2B10CCF5D6B7D74C31C433A081D14BD284F3D2D55F23835CE197094C3C67788404576E5C10DD1C58E60EB6808C4AF5FB54CCF9CC1D0BD2D3D918B2F028D8A42EF0F65BE2ACDC0F6761B7C22957BABB20A501F5A54BF8772F5CB3A87F80023F21A680151F1743ABC6E4B55"
HP_URL = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={}&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
DKHP_URL = 'https://sv.isvnu.vn/dang-ky-hoc-phan.html'   #for worker
LH_URL = "https://sv.isvnu.vn/SinhVienDangKy/GetChiTietLichHoc" 

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
    