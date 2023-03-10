import requests
from bs4 import BeautifulSoup

IDDotDangKy = int(input("Nhap ID cua Hoc Ky: "))

def crawl_lhp_data(start_lhp=1, end_lhp=100):
    base_url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={}&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
    for lhp in range(start_lhp, end_lhp + 1):
        url = base_url.format(IDDotDangKy,lhp, lhp)
        response = requests.post(url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in range(1, 16):
            try:
                tag = soup.find_all('tr')[i]
                attribute = tag['data-guidlhp']
                attribute2 = tag.find_all('div')[1].find('span', text='Mã lớp học phần').next_sibling
                print("GUID: {}".format(attribute),"\n","Ma hoc phan{}".format(attribute2))
            except IndexError:
                break

payload={}
headers = {
  'cookie': 'ASC.AUTH=C755BEDF469030D764CA9EFA3B5F9067E8EB2CECE8C30C1C7365EB0DBBF2725859E0099D6D76321C88CF90ABD53266990D8479247E63757457040F631611FB6DFFF67130DE0A342F3997FE2B30F3ED386EA4680196F761BD1BEE622FD8448C3EA5189E7519ED4BEB7A315283F9430F97D8BF0803E242CC1F4F74C0E4F94F444D',
}

crawl_lhp_data()



