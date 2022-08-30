from bobsled_sdk import BobsledClient

base_url = "https://linkup.bobsled-cloud.com/"

credentials = { "email": "andy@bobsled.co",
        "password": "1WUgbERtARqlhG1I5hAPWzLMSm9T0kU"
}

# Instantiate Client
b = BobsledClient(credentials, base_url)

# Get share object
share = b.get_share('016f3240-2851-11ed-afe0-9922d396a736')

# Create Delivery
folder_contents, size = ["s3://lu-jde-delivery/JDE/Standard/Feeds/"], 2960000000000
delivery = share.create_delivery(folder_contents, size, overwriteMode=True);
delivery.deliver_delivery();
