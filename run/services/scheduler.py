import os
from config import Config
from logging import getLogger

log = getLogger(__name__)


def run():
    if not os.path.exists(Config.get_env("SCHEDULED_UPLOADS_DIR")):
        try:
            os.mkdir(Config.get_env("SCHEDULED_UPLOADS_DIR"))
        except FileExistsError:
            log.error(
                "Failed to create user_files/scheduled directory. Directory already exists."
            )
