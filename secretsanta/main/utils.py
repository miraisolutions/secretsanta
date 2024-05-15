import logging
import time

from pathlib import Path


def setup_logging(level: str = "ERROR"):
    """Sets up logging configuration.

    Args:
        level: logging level
    """
    name_file = f'secretsanta_{time.strftime("%Y%m%d-%H%M%S")}.log'
    log_dir = Path("./log_files/")
    log_dir.mkdir(exist_ok=True)
    path_file = log_dir / name_file
    logging.basicConfig(filename=path_file, level=level, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y/%m/%d %I:%M:%S %p')
