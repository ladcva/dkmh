import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@postgres:5432/dkmh"  # This is for Airflow DB    # For localhost:  "postgresql+psycopg2://admin:1@localhost:5432/dkmh"

POSTGRES_CONN_STRING_SERVER = "postgresql+psycopg2://admin:1@localhost:5433/dkmh"

ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = "5DD0FEAF7D09DB41E6012936C5DB5EF9289B8FCFB3935E7BE5E4E8A43551226A5967E16335DB1641E58AF4A235B0DB2E5F21FFD6D7D8564570C2D91087EBF7006089EC2B1FBF3E9BA7E723233D9D408456B7E5353AE449B35DF66C43059BE09381BA4131025A7BACC6623D386EF1AA8E441397F192F7E961B1916A4CCEB6BB38"
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
    