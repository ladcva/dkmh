# Get constants from config file
from config.default import DEFAULT_NUM_PROCESSES


# Utility functions
def get_num_workers(provided_num_workers):
    try:
        provided_num_workers = int(provided_num_workers)
    except TypeError or ValueError:
        print("Invalid value, \"workers\" must be int.")
        print(f"Using DEFAULT_NUM_PROCESSES={DEFAULT_NUM_PROCESSES} instead.")
        provided_num_workers = DEFAULT_NUM_PROCESSES
    finally:
        if provided_num_workers < DEFAULT_NUM_PROCESSES:
            return provided_num_workers
        else:
            return DEFAULT_NUM_PROCESSES
