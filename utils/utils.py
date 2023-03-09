import requests

# Get constants from config file
from config.default import DEFAULT_NUM_PROCESSES


# Utility functions
def get_num_workers(provided_num_workers):
    try:
        provided_num_workers = int(float(provided_num_workers))
    except TypeError or ValueError:
        print("Invalid value, \"workers\" must be int.")
        print(f"Using DEFAULT_NUM_PROCESSES={DEFAULT_NUM_PROCESSES} instead.")
        provided_num_workers = DEFAULT_NUM_PROCESSES
    finally:
        if provided_num_workers < DEFAULT_NUM_PROCESSES:
            return provided_num_workers
        else:
            return DEFAULT_NUM_PROCESSES

def sort_by_key(unsorted_dict):
    sorted_dict = dict(sorted(unsorted_dict.items()))
    return sorted_dict


def check_cookie(url, cookie):
    # Set the cookie in a session object
    session = requests.Session()
    session.cookies.set('cookie_name', cookie)
    response = session.get(url)
    if response.status_code == 200:
        # If the status code is 200, the cookie is valid
        return True
    else:
        # If the status code is not 200, the cookie is invalid
        return False