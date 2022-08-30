from bobsled_sdk import BobsledClient

base_url = "https://databits.bobsled-cloud.com/"

credentials = { "email": "andy@bobsled.co",
        "password": "8ejq5xS1UlzbRuoN9yulxvk3edhmVAn"
}
# 016f3240-2851-11ed-afe0-9922d396a736
 # Instantiate Client
b = BobsledClient(credentials, base_url)

# Get share object
share = b.create_share()
share.set_overview("Python SDK test", "Delivery test")

# Set share source location
source_locations = share.get_source_locations()
share.set_source_location(source_locations[1]["id"])

# Set share destination location
destination_locations = share.get_destination_locations()
share.set_destination_location("AWS", "us-east-2")

# Create Delivery
folder_contents, size = ["s3://databits-source-us-east-2/stock_data/", "s3://databits-source-us-east-2/danny_sync_folder"], 123456
delivery = share.create_delivery(folder_contents, size, overwriteMode=True);
delivery.deliver_delivery();
