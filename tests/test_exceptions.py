from bobsled_sdk import BobsledClient
from bobsled_sdk import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError
import pytest

base_url = "http://127.0.0.1:3000"

credentials = { "email": "danny@bobsled.co",
        "password": "bobsledding_it"
}

class TestClass:
    def test_bad_credentials(self):
        bad_credentials = { "email": "joe@joe.com",
                        "password": "joe"}
        
        with pytest.raises(BadCredentialsError):
            b = BobsledClient(bad_credentials, base_url)
            
    def test_share_not_found(self):
        b = BobsledClient(credentials, base_url)
        
        with pytest.raises(InternalServerError):
            share = b.get_share("invalid-id")
            
    def test_adding_delivery_before_source_set(self):
        b = BobsledClient(credentials, base_url)
        
        share = b.create_share()
        
        with pytest.raises(InternalServerError):
            share.create_delivery(["some file.txt"])