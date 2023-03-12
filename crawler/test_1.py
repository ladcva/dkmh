import requests, itertools
from config.default import ASC_AUTH_STR


def get_all_subjects():
    list1 = ['INS', 'MAT', 'RUS', 'PSY', 'SOC', 'INE', 'THL', 'FIB', 'PHI', 'PEC', 'HIS', 'POL', 'INT']
    list2 = range(1, 5)
    list3 = range(0, 200)
    codes = ([f"{i}{j}{k:03d}" for i, j, k in itertools.product(list1, list2, list3)])
    return codes

def validate_subject_code(semester_id, subject_code: str):
    url = f"https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={semester_id}&MaMonHoc={subject_code}&DSHocPhanDuocHoc={subject_code}&IsLHPKhongTrungLich=true&LoaiDKHP=1"  #test with a fixed IDDotdangky
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    
    response = requests.post(url, cookies=cookie)

    if "lhpchodangky-notfound" in response.text:
        print(f"{subject_code} does not exist") #testing
        return None
    else:
        print(f"{subject_code} exist") #fetch the code to database
        return subject_code


if __name__ == "__main__":
    codes_list = get_all_subjects()
    available_subject_codes = []

    for subject_code in codes_list:
        current_sbj = validate_subject_code(35, subject_code)
        if subject_code:
            available_subject_codes.append(current_sbj)

    print(available_subject_codes)

#TODO Refactor and use multiprocessing to speed up the process or think of a better way to optimize the process
#TODO Use a database to store the results
#TODO Get all semester IDs and run the process for each semester ID