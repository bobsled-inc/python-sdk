from bobsled import BobsledClient
from bobsled import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError

credentials = { "email": "danny@bobsled.co",
                "password": "bobsledding_it"
                }

try:
    # Instantiate Client
    b = BobsledClient(credentials, "http://127.0.0.1:8080")
    
    # Get share object
    # share = b.create_share()
    share = b.get_share("d1bfd880-0427-11ed-a810-9bdb16485049")
    
    # Set share source location
    source_locations = share.get_source_locations()
    share.set_source_location(source_locations[0])
    
    # Set share destination location
    destination_locations = share.get_destination_locations()
    share.set_destination_location("AWS", "eu-west-1")
    
    # Create Delivery
    print("creating delivery")
    folder_contents = share.get_folder_contents()
    delivery = share.create_delivery(folder_contents)
    
    
    print(delivery)
except BobsledException as err:
    print(type(err))
    print(err.status)
    print(err.data)