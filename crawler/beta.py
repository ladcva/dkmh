import requests
from bs4 import BeautifulSoup
from utils.utils import get_semester_id, get_class_codes
from config.default import ASC_AUTH_STR

def crawl_lhp_data():
    base_url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={}&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
    payload={}
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    for lhp in class_codes:
        url = base_url.format(lastest_sem_id, lhp, lhp)
        response = requests.post(url, cookies=cookie, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in range(1, 16):
            try:
                tag = soup.find_all('tr')[i]
                attribute = tag['data-guidlhp']
                attribute2 = tag.find_all('div')[1].find('span', text='Mã lớp học phần').next_sibling
                print("GUID: {}".format(attribute),"\n","Ma hoc phan{}".format(attribute2))
            except IndexError:
                break


if __name__ == "__main__":
    lastest_sem_id = get_semester_id()[0]
    class_codes = get_class_codes()
    crawl_lhp_data()


