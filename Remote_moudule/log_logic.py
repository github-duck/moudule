import logging
from config import log_path



logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(funcName)s %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
file_handle = logging.FileHandler(log_path)
file_handle.setLevel(logging.INFO)
file_handle.setFormatter(formatter)
stream_handle = logging.StreamHandler()
stream_handle.setLevel(logging.INFO)
stream_handle.setFormatter(formatter)
logger.addHandler(file_handle)
logger.addHandler(stream_handle)


