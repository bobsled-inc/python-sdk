class BobsledException(Exception):
    """
    Error handling in Bobsled is done with exceptions. This class is the base of all exceptions raised by Bobsled.
    """

    def __init__(self, status, data):
        super().__init__()
        self.__status = status
        self.__data = data

class BadCredentialsException(BobsledException):
    """
    Exception raised in case of bad credentials (when Bobsled replies with a 401 or 403 HTML status)
    """