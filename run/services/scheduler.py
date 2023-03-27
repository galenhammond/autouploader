import os
from logging import getLogger

log = getLogger(__name__)


def run():
    if not os.path.exists("./user_files/scheduled"):
        try:
            os.mkdir("./user_files/scheduled")
        except FileExistsError:
            log.error(
                "Failed to create user_files/scheduled directory. Directory already exists."
            )
