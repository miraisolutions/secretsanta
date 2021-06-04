import logging
import time
import os
def setup_logging(level: str = "ERROR"):
    name_file = 'secretsanta_' + time.strftime("%Y%m%d-%H%M%S") +'.log'
    path_file = os.path.join('./log_files/', name_file)
    return logging.basicConfig(filename =path_file, level = level, format = '%(asctime)s %(levelname)s %(message)s',
                               datefmt = '%Y/%m/%d %I:%M:%S %p')