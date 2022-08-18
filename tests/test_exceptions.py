from bobsled_sdk import BobsledClient
from bobsled_sdk import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError
import pytest

base_url = "https://staging-rhizo-co-remix-deploy-remix-app-64ohelifva-ey.a.run.app/"

credentials = { "email": "danny@bobsled.co",
        "password": "bobsledding_it"
}

class TestClass:
    def test_bad_credentials(self):
        bad_credentials = { "email": "joe@joe.com",
                        "password": "joe"}
        
        with pytest.raises(BadCredentialsError):
            b = BobsledClient(bad_credentials, base_url)
            
    def test_invalid_share_id(self):
        b = BobsledClient(credentials, base_url)
        
        with pytest.raises(InternalServerError):
            share = b.get_share("invalid-id")
            
    def test_adding_delivery_before_source_set(self):
        b = BobsledClient(credentials, base_url)
        
        share = b.create_share()
        
        with pytest.raises(InternalServerError):
            share.create_delivery(["some file.txt"], 100)