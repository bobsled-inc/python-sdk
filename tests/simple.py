from bobsled import BobsledClient
from bobsled import BobsledException, BadCredentialsError, InternalServerError, UnknownObjectError

credentials = { "email": "danny@bobsled.co",
                "password": "bobsledding_it"
                }

try:
    # Instantiate Client
    b = BobsledClient(credentials, "http://127.0.0.1:8080")
    print("Client created")
    
    # Get share object
    # share = b.create_share()
    share = b.get_share("86d58ea0-06c5-11ed-a3fb-3d088eb19fb2")
    print("Share acquired")
    
    # Set share source location
    source_locations = share.get_source_locations()
    share.set_source_location(source_locations[0])
    print("Source set")
    
    # Set share destination location
    destination_locations = share.get_destination_locations()
    share.set_destination_location("AWS", "eu-west-1")
    print("Destination set")
    
    # Create Delivery
    print("creating delivery")
    folder_contents = share.get_folder_contents()
    delivery = share.create_delivery(folder_contents)
    print("Delivery created:", delivery)

except BobsledException as err:
    print(type(err))
    print(err.status)
    print(err.data)