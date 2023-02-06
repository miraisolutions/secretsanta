import logging
import time

from pathlib import Path


def setup_logging(level: str = "ERROR"):
    """
    sets up logging configuration.

    :param level: logging level
    """
    name_file = f'secretsanta_{time.strftime("%Y%m%d-%H%M%S")}.log'
    path_file = Path('./log_files/') / name_file
    logging.basicConfig(filename=path_file, level=level, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p')
