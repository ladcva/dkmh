import requests
from bs4 import BeautifulSoup
from config.default import ASC_AUTH_STR

dangky_url = 'https://sv.isvnu.vn/dang-ky-hoc-phan.html'

cookie = {'ASC.AUTH' : ASC_AUTH_STR}

payload = {
    'IDDotDangKy' : 27,
    'IDLoaiDangKy' : 1,
    'GuidIDLopHocPhan': 'W5cD-H286ZsEyCmZ-mJDqw'
}

response = requests.post(dangky_url, cookies=cookie, data=payload)
print(response.text)


# For each user's request in queue, we need to:
    # 1. Get the user's cookie
    # 2. Get the user's class codes
    # 3. Run the register function for each class code