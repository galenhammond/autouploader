from enum import Enum


class UploadPolicy(Enum):
    UPLOAD_IF_NEW = 1
    UPLOAD_FROM_QUEUE = 2
    NEVER_UPLOAD = 3
