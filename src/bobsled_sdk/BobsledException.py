class BobsledException(Exception):
    """
    Error handling in Bobsled is done with exceptions. This class is the base of all exceptions raised by Bobsled.
    """

    def __init__(self, status, data):
        super().__init__()
        self.__status = status
        self.__data = data
        
    @property
    def status(self):
        """
        The status returned by the Bobsled API
        """
        return self.__status

    @property
    def data(self):
        """
        The data returned by the Bobsled API
        """
        return self.__data

class BadCredentialsError(BobsledException):
    """
    Exception raised in case of bad credentials (when Bobsled replies with a 401 or 403 HTML status)
    """
    
class InternalServerError(BobsledException):
    """
    Exception raised when something cannot be resolved in the internal server (when Bobsled replies with a 500 HTML status)
    """
    
class UnknownObjectError(BobsledException):
    """
    Exception raised when requested object is not found (when Bobsled replies with a 404 HTML status)
    """
    
class UnprocessableEntityError(BobsledException):
    """
    Exception raised when the server receives invalid input (when Bobsled repleis with a 422 HTML Status)
    """