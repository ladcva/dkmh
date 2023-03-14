import requests, itertools, time
from config.default import ASC_AUTH_STR
from multiprocessing import Pool, cpu_count
from functools import partial

available_subject_codes = []

def get_all_subjects():
    list1 = ['INS', 'MAT', 'RUS', 'PSY', 'SOC', 'INE', 'THL', 'FIB', 'PHI', 'PEC', 'HIS', 'POL', 'INT', 'FLF', 'VLF', 'ENG', 'LIN', 'MNS', 'BSA']
    list2 = range(1, 5)
    list3 = range(0, 200)
    codes = ([f"{i}{j}{k:03d}" for i, j, k in itertools.product(list1, list2, list3)])
    return codes


def validate_subject_code(semester_id, subject_code: str):
    url = f"https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={semester_id}&MaMonHoc={subject_code}&DSHocPhanDuocHoc={subject_code}&IsLHPKhongTrungLich=true&LoaiDKHP=1"  #test with a fixed IDDotdangky
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    
    response = requests.post(url, cookies=cookie)

    if "lhpchodangky-notfound" in response.text:    # Only return codes that are existed
        return None
    else:
        print(f"{subject_code} exist") #fetch the code to database
        return subject_code


if __name__ == "__main__":
    start_time = time.time()
    codes_list = get_all_subjects()
    num_processes = cpu_count()  # Get number of CPU cores available
    chunk_size = len(codes_list) // num_processes  # Determine chunk size for each process

    with Pool(processes=num_processes) as pool:
        func = partial(validate_subject_code, 35)   # Create a partial func to pass semester_id to validate_subject_code
        for result in pool.imap_unordered(func, codes_list, chunksize=chunk_size): # Dont need ordered results, so imap_unordered will gain performance
            if result:
                available_subject_codes.append(result)

    print(available_subject_codes)
    end_time = time.time()
    print(f"Processing time: {end_time - start_time} seconds")

    
#TODO Refactor and use multiprocessing to speed up the process or think of a better way to optimize the process -> partially done, multiprocessing implemented
#TODO Use a database to store the results
#TODO Get all semester IDs and run the process for each semester ID