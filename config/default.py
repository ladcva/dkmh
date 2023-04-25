import os

DEFAULT_NUM_PROCESSES = os.cpu_count()  # e.g. Apple M1 -> DEFAULT_NUM_PROCESSES = 8
POSTGRES_CONN_STRING = "postgresql+psycopg2://admin:1@localhost:5432/dkmh"
ISVNU_DASHBOARD_URL = 'https://sv.isvnu.vn/dashboard.html'
ASC_AUTH_STR = '22E4089D4C994342E413EAC33787E348BBC6D1D257AD4054574E046D18674F5606F3B2F75210BD6FFC249915CD2BF1D3F4DB4A0D9B437736841690A2FE97BBB16DB7A2C6A2CFEF11FC619EA4C184A0FB18649BA9211F3E7CA2693494A6DFC6AA413B2114E11947EC85CB35FE55E0B9EAC13D35C142EA9A228DCAE28C00E27A96'
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
    