from enum import Enum


class Status(Enum):
    SUCCESS = "Success"
    PERMISSION_DENIED = "Permission Denied"
    BAD_REQUEST = "Bad Request"
    NOT_FOUND = "Not Found"
