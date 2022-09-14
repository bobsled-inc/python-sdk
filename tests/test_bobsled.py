from bobsled_sdk import BobsledClient
from bobsled_sdk import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError
from dotenv import dotenv_values

config = dotenv_values(".env")
base_url = config["STAGING_URL"]
credentials = { "email": config["STAGING_EMAIL"],
        "password": config["STAGING_PASSWORD"]
}

class TestClass:
    def test_create_delivery(self):
        
        # Instantiate Client
        b = BobsledClient(credentials, base_url)
        
        # Get share object
        share = b.create_share()
        share.set_overview("Delivery test", "Delivery test")
        
        # Set share source location
        source_locations = share.get_source_locations()
        share.set_source_location(source_locations[0]["id"])
        
        # Set share destination location
        destination_locations = share.get_destination_locations()
        share.set_destination_location("AWS", "eu-west-1")
        
        # Create Delivery
        folder_contents, size = ["s3://rhizo-your-bucket-name/folder/folder-2/folder-3/folder-4/again-file.csv","s3://rhizo-your-bucket-name/folder/other-file.csv","s3://rhizo-your-bucket-name/foo/bar/foo/bar/foo/bar.txt"], 137035
        delivery = share.create_delivery(folder_contents, size)
        
        # Check Delivery Status
        print(delivery.status())
        
        # Delivering the Delivery
        delivery.deliver_delivery()
        
        # Access the delivery
        url = delivery.access()
        print(url)
        
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
        
        folder_contents, size = share.get_all_files()
        delivery = share.create_delivery(folder_contents, size)
        
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
        # testing share update function
        b = BobsledClient(credentials, base_url)
        
        share = b.create_share()
        
        source_locations = share.get_source_locations()
        
        name = "python test"
        description = "a description"
        source_id = source_locations[0]["id"]
        destination_cloud = "AWS"
        destination_region = "eu-west-1"
        
        params = {
            "name": name,
            "description": description,
            "locationId": source_id,
            "cloud": destination_cloud,
            "region": destination_region
        }
        
        share.update(params)
        
        share_information = share.get_share_information()
        assert name == share_information["share"]["name"]
        assert description == share_information["share"]["description"]
        assert source_id == share_information["share"]["sourceLocation"]["id"]
        assert destination_cloud  == share_information["share"]["destinationLocation"]["cloud"]
        assert destination_region ==  share_information["share"]["destinationLocation"]["region"]
        
        share.archive()
        
    def test_access_identifiers(self):
        
        b = BobsledClient(credentials, base_url)
        share = b.create_share()
        
        share.set_overview("arn test", "python driver")
        
        source_locations = share.get_source_locations()
        source_id = source_locations[0]["id"]
        share.set_source_location(source_id)
        
        destination_locations = share.get_destination_locations()
        destination_cloud = "AWS"
        destination_region = "eu-west-1"
        share.set_destination_location(destination_cloud, destination_region)
        
        ARN_list = ["arn:aws:iam::123678912012:user/*", "arn:aws:iam::123698912012:user/*", "arn:aws:iam::123699912012:user/*"]
        share.add_access_identifiers(ARN_list)