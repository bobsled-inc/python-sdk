from bobsled import BobsledClient
from bobsled import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError
import pytest

base_url = "http://127.0.0.1:8080"

class TestClass:
    
    
    def test_create_delivery(self):
        
        credentials = { "email": "danny@bobsled.co",
                "password": "bobsledding_it"
        }
        
        # Instantiate Client
        b = BobsledClient(credentials, base_url)
        
        # Get share object
        # share = b.create_share()
        share = b.get_share("86d58ea0-06c5-11ed-a3fb-3d088eb19fb2")
        
        # Set share source location
        source_locations = share.get_source_locations()
        share.set_source_location(source_locations[0])
        
        # Set share destination location
        destination_locations = share.get_destination_locations()
        share.set_destination_location("AWS", "eu-west-1")
        
        # Create Delivery
        folder_contents = share.get_folder_contents()
        delivery = share.create_delivery(folder_contents)
        
        # Delivering the Delivery
        delivery.deliver_delivery()
        print("Delivery delivered")
        
    def test_bad_credentials(self):
        credentials = { "email": "joe@joe.com",
                        "password": "joe"}
        
        with pytest.raises(BadCredentialsError):
            BobsledClient(credentials, base_url)