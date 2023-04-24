from multiprocessing.process import BaseProcess
from random import randrange
from time import sleep
from datetime import datetime
from uuid import uuid4
import requests



class Worker(BaseProcess):
    """
        This constructor defines tasks that will be executed in the workers.
        """
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def task(cls, auth_user, value):
        task_uuid = uuid4()

        dangky_url = 'https://sv.isvnu.vn/dang-ky-hoc-phan.html'

        cookie = {'ASC.AUTH' : auth_user}
        
        payload = {
            'IDDotDangKy' : 35, # Need to change this also
            'IDLoaiDangKy' : 1,
            'GuidIDLopHocPhan': value
        }

        response = requests.post(dangky_url, cookies=cookie, data=payload)
        

        datetime_now = datetime.now().strftime("%H:%M:%S")
        print(f'Task {task_uuid} with object {value} executing at {datetime_now}, auth_user = {auth_user}', flush=True)

        # execution_time = randrange(start=3, stop=7)
        # sleep(execution_time)
        print(f"Completed - Task {task_uuid}")
        if "Có lỗi xảy ra" in response.text:
            return f"Failed to register {value} !"
        else:
            return f"Successfully registered {value} !"

