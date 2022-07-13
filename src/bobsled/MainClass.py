import requests

from bobsled.utils import flatten
from . import BobsledException

class BobsledClient:
    """
    This is the main class you instantiate to access Bobsled. 
    """
    
    def __init__(self, credentials, base_url = "http://127.0.0.1:8080"):
        self.credentials = credentials
        self.base_url = base_url
        self.s = requests.Session()
        headers = {
            "User-Agent": "Bobsled-Python-SDK/Python",
        }
        self.s.headers.update(headers)
        
        params = {
            "_data": "routes/testing/signInWithEmailAndPassword"
        }
        
        response = self.s.post(
            "http://127.0.0.1:3000" + "/testing/signinwithemailandpassword?_data=routes%2Ftesting%2FsignInWIthEmailAndPassword",
            data=self.credentials)
        if response.status_code != 204:
            raise BobsledException.BadCredentialsException(status = response.status_code, data = response.text)

    def list_shares(self):
        params = {
            "_data": "routes/__auth/shares/index"
        }
        
        r = self.s.get(
            self.base_url,
            params=params
        )
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
            return []
        json_shares = r.json()['shares']
        share_list_ids = []
        for share in json_shares:
            share_list_ids.append(share['id'])
        return share_list_ids

    def get_share(self, share_id):
        return self.Share(share_id, self.s, self.base_url)

    def create_share(self):
        params = {
            "index" : "",  # We need this for some reason
            "_data": "routes/__auth/shares/index"
        }
        
        r = self.s.post(self.base_url +
                        "/shares?index=&_data=routes%2F__auth%2Fshares%2Findex")
        if r.status_code != 204:
            print("Failed to create share", r.status_code)
            return
        header_str = r.headers["x-remix-redirect"]
        share_id = header_str[8:]
        print("Created a share with id of:", share_id, "\n")
        return self.Share(share_id, self.s, self.base_url)


    class Share:
        def __init__(self, share_id, session, base_url):
            self.share_id = share_id
            self.s = session
            self.base_url = base_url

        def get_id(self):
            return self.share_id

        def change_overview(self, name, description):
            """Changes overview text of the share
            
            :calls: `GET /shares/{share_id}/overview`
            """
        
            data = {
                "name": name,
                "description": description
            }
            
            params = {
                "_data": "routes/shares/shareId/overview"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/overview",
                data=data,
                params=params)
            if r.status_code != 204:
                print("error")
                return

        def get_source_locations(self):
            """ Retrieves and returns location_ids that can be used in set_source_location
            
            :calls: `GET /shares/{share_id}/source`
            :return: list of location_ids
            """
            
            params = {
                "_data": "routes/__auth/shares/shareId/source"
            }
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/source",
                params=params)
            print(r.status_code)
            if r.status_code != 200:
                return []
            json_locations = r.json()['locations']
            locations_list_ids = []
            for location in json_locations:
                locations_list_ids.append(location['id'])
            return locations_list_ids

        def set_source_location(self, location_id):
            """Set the source of the share to location_id

            :param location_id: unique identifier of a source container
            """            
            data = {"locationId": location_id}
            params = {
                "_data": "routes/__auth/shares/shareId/source"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/source",
                data=data,
                params=params)
            if r.status_code != 204:
                print("error")
                return

        # Gets list of destination location ids
        def get_destination_locations(self):
            
            params = {
                "_data": "routes/__auth/shares/shareId/destination/new"
            }
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/destination/new",
                params=params
            )
            if r.status_code != 200:
                print(r.status_code, r.text)
                return []
            locations = r.json()['availableAwsRegions']
            return locations

        # Change destination bucket to given location_id
        def set_destination_location(self, location_id):
            data = {"cloud": "AWS", "region": location_id}
            params = {
                "_data": "routes/__auth/shares/shareId/destination/new"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/destination/new",
                data=data,
                params=params)
            if r.status_code != 204:
                print("error")
                return
            print("Destination location changed to:", location_id)
            print()

        # Returns a list of available file paths
        def get_folder_contents(self):
            params = {
                "_data": "routes/__auth/shares/shareId/loadCloudData"
            }
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/loadCloudData",
                params=params)
            if r.status_code != 200:
                print("Cannot get folder contents", r.status_code)
                return []
            print(r.json())
            folderContents = r.json()['folderContents']
            # figure out a better way to flatten maybe?
            return flatten(folderContents)

        def get_deliveries(self):
            r = self.s.get(self.base_url + "/shares/" + self.share_id +
                "/driver")
            #print(r.text)
            delivery_list = []
            for obj in r.json():
                delivery_list.append(self.Delivery(obj["id"], self.share_id, self.s, self.base_url))
            return delivery_list

        # Creates a delivery given selection of file paths in the source bucket
        def create_delivery(self, selection):
            # if selection is a single string, then we have to handle differently

            data = {
                "sharedFiles": selection.__str__().replace(" ", "").replace(
                    "\'", "\"")  # we have to fit specific format
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/delivery?_data=routes%2F__auth%2Fshares%2F%24shareId%2Fdelivery",
                data=data)
            if r.status_code != 204:
                print("Failed to create Delivery", r.status_code)
                return
            print("Delivery created:", selection)
            print()
            # hopefully we can return delivery_id

        # Creates a delivery given selection of file paths in the source bucket
        def create_delivery_test(self, selection):
            # if selection is a single string, then we have to handle differently

            data = {
                "sharedFiles": selection.__str__().replace(" ", "").replace(
                    "\'", "\"")  # we have to fit specific format
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/driver",
                data=data)
            if r.status_code != 200:
                print("Failed to create Delivery", r.status_code)
                return
            print(r.json())
            print("Delivery id:", r.json()["delivery_id"])
            return self.Delivery(r.json()["delivery_id"], self.share_id, self.s, self.base_url)
            # print("Delivery id:", r.json()["id"])
            # hopefully we can return delivery_id

        # Gets a dictionary of Providers and Consumers
        def get_team(self):
            params = {
                "_data": "routes/__auth/shares/shareId/team"
            }
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/team",
                params=params)
            if r.status_code != 200:
                print("error")
                return
            return r.json()

        # Add a Consumer using email
        def add_consumer(self, consumer_email):
            data = {
                "email": consumer_email,
                "role": "consumer",
                "actionType": "addUserToShare"
            }
            params = {
                "_data": "routes/__auth/shares/shareId/team"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/team",
                data=data,
                params=params)
            if r.status_code != 200:
                print("Cannot add consumer", r.status_code, r.text)
                return
            print(consumer_email, "added as a consumer")

        def send_invitation(self, id):
            # Provide email, calls getTeam to get according id, then POSTs to the right id?
            return "unimplemented"

        def edit_access_identifiers(self, ARN_list):
            data = {
                "accessIdentifiers": ARN_list.__str__().replace(" ", "").replace(
                    "\'", "\"")
            }
            params = {
                "_data": "routes/__auth/shares/shareId/destination/edit"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/destination/edit",
                data=data)
            if r.status_code != 204:
                print("Cannot add ARN")
                print(r.status_code)
                print(r.text)
                return

        class Delivery:
            def __init__(self, delivery_id, share_id, session, base_url):
                # Maybe also store delivery name? 
                self.delivery_id = delivery_id
                self.share_id = share_id
                self.s = session
                self.base_url = base_url
            
            def __str__(self):
                # Use delivery name instead of id
                return "Delivery(" + self.delivery_id + ")"

            def __repr__(self):
                return "Delivery(" + self.delivery_id + ")"

            def deliver_delivery(self):
                data = {
                    "deliverDeliveryId": self.delivery_id
                }
                params = {
                    "_data": "routes/__auth/shares/shareId"
                }
                r = self.s.post(
                    self.base_url + "/shares/" + self.share_id,
                    data=data,
                    params=params)
                if not (200 <= r.status_code < 300):
                    print("Delivery failed")
                    return
                print("Delivery succeeded")

            def edit_delivery(self):
                # Unimplemented
                return