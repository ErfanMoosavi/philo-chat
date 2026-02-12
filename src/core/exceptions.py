class PhiloChatError(Exception):
    pass


class BadRequestError(PhiloChatError):
    pass


class NotFoundError(PhiloChatError):
    pass


class PermissionDeniedError(PhiloChatError):
    pass


class LLMError(PhiloChatError):
    pass
