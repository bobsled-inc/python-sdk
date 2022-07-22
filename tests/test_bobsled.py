from bobsled import BobsledClient
from bobsled import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError
import pytest

base_url = "http://127.0.0.1:8080"

credentials = { "email": "danny@bobsled.co",
        "password": "bobsledding_it"
}

class TestClass:
    def test_create_delivery(self):
        
        # Instantiate Client
        b = BobsledClient(credentials, base_url)
        
        # Get share object
        share = b.create_share()
        
        # Set share source location
        source_locations = share.get_source_locations()
        share.set_source_location(source_locations[0]["id"])
        
        # Set share destination location
        destination_locations = share.get_destination_locations()
        share.set_destination_location("AWS", "eu-west-1")
        
        # Create Delivery
        folder_contents = share.get_folder_contents()
        delivery = share.create_delivery(folder_contents)
        
        # Delivering the Delivery
        delivery.deliver_delivery()
        
    def test_asserts(self):
        # Set some things, then get share and see if they have been changed properly
        b = BobsledClient(credentials, base_url)
        
        share = b.create_share()
        
        name = "testing"
        description = "a description"
        share.set_overview(name, description)
        
        source_locations = share.get_source_locations()
        source_id = source_locations[0]["id"]
        share.set_source_location(source_id)
        
        destination_locations = share.get_destination_locations()
        destination_cloud = "AWS"
        destination_region = "eu-west-1"
        share.set_destination_location(destination_cloud, destination_region)
        
        folder_contents = share.get_folder_contents()
        delivery = share.create_delivery(folder_contents)
        
        user_email = "test@test.com"
        share.add_consumer(user_email)
        
        share_information = share.get_share_information()
        
        assert share.share_id == share_information["share"]["id"]
        assert name == share_information["share"]["name"]
        assert description == share_information["share"]["description"]
        assert source_id == share_information["share"]["sourceLocation"]["id"]
        assert destination_cloud  == share_information["share"]["destinationLocation"]["cloud"]
        assert destination_region ==  share_information["share"]["destinationLocation"]["region"]
        assert delivery.delivery_id == share_information["deliveries"][0]["id"]
        assert folder_contents == share_information["deliveries"][0]["sharedFiles"]
        assert user_email == share_information["consumers"][0]["user"]["email"]
        
    def test_update(self):
        b = BobsledClient(credentials, base_url)
        
        share = b.create_share()
        
        source_locations = share.get_source_locations()
        source_id = source_locations[0]["id"]
        
        params = {
            "name": "python test",
            "description": "a description",
            "locationId": source_id,
            "cloud": "AWS",
            "region": "eu-west-1"
        }
        share.update(params)