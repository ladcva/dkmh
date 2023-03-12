import requests, itertools
from config.default import ASC_AUTH_STR


def subjects_crawler():
    list1 = ['INS', 'MAT', 'RUS', 'PSY', 'SOC', 'INE', 'THL', 'FIB', 'PHI', 'PEC', 'HIS', 'POL', 'INT']
    list2 = range(1, 5)
    list3 = range(0, 200)
    codes = ([f"{i}{j}{k:03d}" for i, j, k in itertools.product(list1, list2, list3)])
    return codes

codes_list = subjects_crawler()

def validate_subject_code():
    base_url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"  #test with a fixed IDDotdangky
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    for code in codes_list:
        url = base_url.format(code, code)
        response = requests.post(url, cookies=cookie)

        if "lhpchodangky-notfound" in response.text:
            print("Subject code does not exist") #testing
        else:
            print("Subject code exist") #fetch the code to database


# Test
base_url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc={}&DSHocPhanDuocHoc={}&IsLHPKhongTrungLich=true&LoaiDKHP=1"  #test with a fixed IDDotdangky
cookie = {'ASC.AUTH': ASC_AUTH_STR}
url = base_url.format("INS3069", "INS3069")
response = requests.post(url, cookies=cookie)

if "lhpchodangky-notfound" in response.text:
    print("Subject code does not exist") #testing
else:
    print("Subject code exist") #fetch the code to database

print(subjects_crawler())
print(f"Total {len(subjects_crawler())} subjects to iterate")