from bobsled_sdk import BobsledClient
from bobsled_sdk import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError
import pytest

base_url = "http://127.0.0.1:8080"

credentials = { "email": "danny@bobsled.co",
        "password": "bobsledding_it"
}

class TestClass:
    def test_bad_credentials(self):
        credentials = { "email": "joe@joe.com",
                        "password": "joe"}
        
        with pytest.raises(BadCredentialsError):
            b = BobsledClient(credentials, base_url)
            
    def test_share_not_found(self):
        b = BobsledClient(credentials, base_url)
        
        with pytest.raises(UnknownObjectError):
            share = b.get_share("invalid-id")