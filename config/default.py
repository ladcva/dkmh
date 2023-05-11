import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@localhost:5432/dkmh"
ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = "E21700CD4E6CA4BB362791CB092BC923FC79847D8A27F002B218C975ACC4C160600000F842EC26858716AF3151D0C1C9B4B9862F607DDEDFA71FBF35A00123AFDC0DD7979BF922D124E5001FE20CD0FF98694ADC2270BDF2A44EEDEF5DD06E8C781A901E9DB63018701BC6C64C9DB25CBD7DCDC7A329CE2E02B18E607C203A5F"
DKHP_URL = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={}&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
LH_URL = "https://sv.isvnu.vn/SinhVienDangKy/GetChiTietLichHoc" #Lich Hoc url

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
    