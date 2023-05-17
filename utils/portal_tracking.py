from utils.utils import get_semester_id
from config.default import ASC_AUTH_STR
import requests

def check_portal_open():
    url = "https://sv.isvnu.vn/SinhVienDangKy/CheckDotChoPhepDangKy"
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    payload = {'param%5BIDDotDangKy%5D': get_semester_id()[0]}
    response = requests.post(url, cookies=cookie, data=payload)
    if "không hợp lệ" in response.text:
        print("Portal is closed")
    else:
        print("Portal is open")

if __name__ == "__main__":    
    check_portal_open()