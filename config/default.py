import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
PROCESSES_FACTOR = 3  # Number of processes to run in parallel e.g. Apple M1 has 8 cores -> 8*3 = 24 processes
NUM_PROCESSES = DEFAULT_NUM_PROCESSES * PROCESSES_FACTOR
POSTGRES_CONN_STRING =  os.environ["POSTGRES_CONN_STRING"] # This is for Airflow DB
POSTGRES_CONN_STRING_SERVER = os.environ["POSTGRES_CONN_STRING_SERVER"]

ISVNU_DASHBOARD_URL = "https://sv.isvnu.vn/dashboard.html"
ASC_AUTH_STR = os.environ["ASC_AUTH_STR"]
HP_URL = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={}&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
DKHP_URL = "https://sv.isvnu.vn/dang-ky-hoc-phan.html"  # for worker
LH_URL = "https://sv.isvnu.vn/SinhVienDangKy/GetChiTietLichHoc"


class DefaultConfig(object):
    """Flask configuration."""

    TESTING = True
    DEBUG = True
    ENV = "development"
    SECRET_KEY = os.environ["FLASK_SECRET"]
    CACHE_TYPE = "simple"


class PgConnection:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def conn_string(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"