import requests
from config.default import ASC_AUTH_STR


codes = []
def subjects_crawler():
    list1 = ['INS', 'MAT', 'RUS', 'PSY', 'SOC', 'INE', 'THL', 'FIB', 'PHI', 'PEC', 'HIS', 'POL', 'INT']
    # list2 = range(1,8)
    list3 = range(1000, 7999)

    for i in list1:
        for j in list3:
            codes.append(i+str(j))

    print(codes[:20])

def validate_subject_code():
    base_url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"  #test with a fixed IDDotdangky
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    for code in codes:
        url = base_url.format(code, code)
        response = requests.post(url, cookies=cookie)

        if "lhpchodangky-notfound" in response.text:
            print("Subject code does not exist") #testing
        else:
            print("Subject code exist") #fetch the code to database


#Test
base_url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"  #test with a fixed IDDotdangky
cookie = {'ASC.AUTH': ASC_AUTH_STR}
url = base_url.format("INS3069", "INS3069")
response = requests.post(url, cookies=cookie)

if "lhpchodangky-notfound" in response.text:
    print("Subject code does not exist") #testing
else:
    print("Subject code exist") #fetch the code to database