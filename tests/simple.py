from bobsled import BobsledClient

credentials = { "email": "danny@bobsled.co",
                "password": "bobsledding_it"
                }
b = BobsledClient(credentials, "http://127.0.0.1:8080")
# share = b.create_share()
share = b.get_share("cde7ae00-0390-11ed-8aa7-058df2bd29cc")
folder_contents = share.get_folder_contents()
delivery = share.create_delivery(folder_contents)
print(delivery)