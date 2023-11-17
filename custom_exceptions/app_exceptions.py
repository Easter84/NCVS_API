class AppBasicException(Exception):
    pass

class NoResponseException(AppBasicException):
    pass

class InvalidDataException(AppBasicException):
    pass