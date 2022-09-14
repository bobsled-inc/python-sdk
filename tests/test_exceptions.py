from bobsled_sdk import BobsledClient
from bobsled_sdk import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError, UnprocessableEntityError
import pytest
from dotenv import dotenv_values

config = dotenv_values(".env")
base_url = config["STAGING_URL"]
credentials = { "email": config["STAGING_EMAIL"],
        "password": config["STAGING_PASSWORD"]
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
            
    def test_invalid_arns(self):
        b = BobsledClient(credentials, base_url)
        
        share = b.create_share()
        
        with pytest.raises(UnprocessableEntityError): # raises 422
            share.set_destination_location("AWS", "eu-west-1")
            share.add_access_identifiers(["baaaaad-arn", "this-one-too"])