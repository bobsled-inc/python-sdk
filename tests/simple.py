from bobsled import BobsledClient

credentials = { "email": "danny@bobsled.co",
                "password": "bobsledding_it"
                }
b = BobsledClient(credentials, "http://127.0.0.1:8080")
b.list_shares()
# new_share = b.createShare()
new_share = b.getShare("9ba49de0-fd5f-11ec-becd-1d22c5f1371e")
new_share.changeOverview("testing", "bobsledding it")
source_locations = new_share.getSourceLocations()
print("Source locations:", source_locations)
new_share.changeSourceLocation(source_locations[0])
destination_locations = new_share.getDestinationLocations()
print(destination_locations)
new_share.changeDestinationLocation(destination_locations[0])
folderContents = new_share.getFolderContents()
print(folderContents, "\n")
delivery_1 = new_share.createDeliveryTest(folderContents)
delivery_2 = new_share.createDeliveryTest(folderContents)
delivery_3 = new_share.createDeliveryTest(folderContents)
# delivery_1.deliverDelivery()
l = new_share.getDeliveries()
print(l)
new_share.addConsumer("danny@bobsled.co")
new_share.editARNs(["test", "test1", "test2"])
print(new_share.getTeam())