from multiprocessing.process import BaseProcess
from datetime import datetime
from uuid import uuid4
import requests
from utils.utils import get_semester_id


class Worker(BaseProcess):
    """
        This constructor defines tasks that will be executed in the workers.
        """
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def task(cls, auth_user, guid, queuedClass):
        start_time = datetime.now()
        task_uuid = uuid4()

        dangky_url = 'https://sv.isvnu.vn/dang-ky-hoc-phan.html'
        cookie = {'ASC.AUTH' : auth_user}
        payload = {
            'IDDotDangKy' : get_semester_id()[1], # index 1 for testing
            'IDLoaiDangKy' : 1, # Maybe this if our users stoopid
            'LHP': queuedClass,
            'GuidIDLopHocPhan': guid
        }
        response = requests.post(dangky_url, cookies=cookie, data=payload)

        datetime_now = datetime.now().strftime("%H:%M:%S")
        print(f'Task {task_uuid} with object {guid} executing at {datetime_now}, auth_user = {auth_user}', flush=True)

        print(f"Completed - Task {task_uuid}, in {datetime.now() - start_time} seconds")

        print(payload)              # For debugging
        print(response.text)
        
        if "Có lỗi xảy ra" or None in response.text:
            return f"Failed to register class {queuedClass} {guid} !"
        else:
            return f"Successfully registered class{queuedClass} {guid} !"

