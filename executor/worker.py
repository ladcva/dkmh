from multiprocessing.process import BaseProcess
from datetime import datetime
from uuid import uuid4
from utils.utils import get_semester_id_worker, file_logger
from config.default import DKHP_URL
import requests

class Worker(BaseProcess):
    """
        This constructor defines tasks that will be executed in the workers.
        """
    def __init__(self) -> None:
        super().__init__()              #TODO: wrapper or retry, limit, error code, retry conditions, Stateful

    @classmethod                                        #TODO: Implement Wrapper
    def task(cls, auth_user, guid, queuedClass):
        start_time = datetime.now()
        task_uuid = uuid4()

        cookie = {'ASC.AUTH' : auth_user}
        payload = {
            'IDDotDangKy' : str(get_semester_id_worker()[0]), # index 1 for testing
            'IDLoaiDangKy' : 1, # Maybe this if our users stoopid
            'LHP': queuedClass,
            'GuidIDLopHocPhan': guid
        }
        response = requests.post(DKHP_URL, cookies=cookie, data=payload)

        datetime_now = datetime.now().strftime("%H:%M:%S")
        print(f'Task {task_uuid} with object {guid} executing at {datetime_now}, auth_user = {auth_user}', flush=True)
        print(f"Completed - Task {task_uuid}, in {datetime.now() - start_time} seconds")

        print(payload)              # For debugging
        print(response.text)
        
        while "Có lỗi xảy ra" or None in response.text:
            file_logger.error(f"Failed to register class {queuedClass} with GUID: {guid} for user with auth: {auth_user} !")
            return f"Failed to register class {queuedClass} {guid} !"

        if "Bạn đã đăng ký thành công" in response.text:
            file_logger.info(f"Successfully registered class {queuedClass} with GUID: {guid} for user with auth: {auth_user} !")
            return f"Successfully registered class{queuedClass} {guid} !"

