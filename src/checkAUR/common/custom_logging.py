"""Logger module for the entire project
"""

import logging


def gen_logger():
    """generate logger for the entire project

    Returns:
        logging.Logger: logger to be used
    """
    log = logging.getLogger("checkAUR_log")
    if __debug__:
        log.setLevel(logging.DEBUG)
        log.debug("**** DEBUG ****")
    else:
        log.setLevel(logging.WARNING)

    file_han = logging.FileHandler("logs.log")
    log.addHandler(file_han)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_han.setFormatter(formatter)

    return log

logger = gen_logger()
