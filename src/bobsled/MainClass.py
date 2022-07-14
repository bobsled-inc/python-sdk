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
            "http://127.0.0.1:3000" + "/testing/signinwithemailandpassword",
            data=self.credentials,
            params=params)
        if response.status_code != 204:
            raise BobsledException.BadCredentialsException(status = response.status_code, data = response.text)

    def list_shares(self):
        """Returns a list of share_ids that can be used with get_share

        :calls: `GET /shares`
        :return: a list of share_ids
        """        
        params = {
            "_data": "routes/__auth/shares/index"
        }
        
        r = self.s.get(
            self.base_url +"/shares",
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
        """Returns the Share with given share_id

        :param share_id: unique id of share
        :return: Share object
        """        
        return self.Share(share_id, self.s, self.base_url)

    def create_share(self):
        """Creates a new share. This only works if authenticated as a provider

        :calls: `POST /shares`
        :return: the Share object representing the share that was just created
        """        
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
        """
        This class represents a share, and should only be acquired by the user through calling get_share or create_share on a BobsledClient
        """
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
                "_data": "routes/shares/$shareId/overview"
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
                "_data": "routes/__auth/shares/$shareId/source"
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

            :calls: `POST /shares/{share_id}/source`
            :param location_id: unique identifier of a source container
            """            
            data = {"locationId": location_id}
            params = {
                "_data": "routes/__auth/shares/$shareId/source"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/source",
                data=data,
                params=params)
            if r.status_code != 204:
                print("error")
                return

        def get_destination_locations(self):
            """Get destination locations that can be used in set_destination_location

            :calls: `GET /shares/{share_id}/destination/new`
            :return: something, a list or dictionary of locations, undecided
            """            
            
            params = {
                "_data": "routes/__auth/shares/$shareId/destination/new"
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

        def set_destination_location(self, location_id):
            """Sets destination location of this share to given cloud and location_id (region?)

            :calls: `POST /shares/{share_id}/destination/new`
            :param location_id: something
            """            
            data = {"cloud": "AWS", "region": location_id}
            params = {
                "_data": "routes/__auth/shares/$shareId/destination/new"
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

        def get_folder_contents(self):
            """Returns flattened contents of all files in source location

            :calls: `GET /shares/{share_id}/loadCloudData`
            :return: list of file paths
            """            
            params = {
                "_data": "routes/__auth/shares/$shareId/loadCloudData"
            }
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/loadCloudData",
                params=params)
            if r.status_code != 200:
                print("Cannot get folder contents", r.status_code)
                return []
            folderContents = r.json()['folderContents']
            return flatten(folderContents)

        # NEED TO CHANGE THIS
        def get_deliveries(self):
            """Returns the list of deliveries of this share

            :calls: `GET /shares/{share_id}/driver`
            :return: list of deliveries
            """            
            r = self.s.get(self.base_url + "/shares/" + self.share_id +
                "/driver")
            delivery_list = []
            for obj in r.json():
                delivery_list.append(self.Delivery(obj["id"], self.share_id, self.s, self.base_url))
            return delivery_list

        def create_delivery(self, selection):
            """Creates and returns a Delivery object given selection of file paths

            :calls: `POST /shares/{share_id}/delivery`
            :param selection: file paths for files in the source container to be included in this delivery
            """            

            data = {
                "sharedFiles": selection.__str__().replace(" ", "").replace(
                    "\'", "\"")  # we have to fit specific format
            }
            params = {
                "_data": "routes/__auth/shares/$shareId/delivery"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/delivery",
                data=data,
                params=params)
            if r.status_code != 200:
                print("Failed to create Delivery", r.status_code)
                return
            return self.Delivery(r.json()["delivery_id"], self.share_id, self.s, self.base_url)

        def get_team(self):
            """Returns team members

            :calls: `GET /shares/{share_id}/team`
            :return: dictionary representing team members
            """            
            params = {
                "_data": "routes/__auth/shares/$shareId/team"
            }
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/team",
                params=params)
            if r.status_code != 200:
                print("error")
                return
            return r.json()

        def add_consumer(self, consumer_email):
            """Adds a consumer by given email

            :calls: `POST /shares/{share_id}/team`
            :param consumer_email: email address of the consumer to be added
            """            
            data = {
                "email": consumer_email,
                "role": "consumer",
                "actionType": "addUserToShare"
            }
            params = {
                "_data": "routes/__auth/shares/$shareId/team"
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
            # Unimplemented
            pass

        def edit_access_identifiers(self, ARN_list):
            """Edit access identifiers of this share

            :param ARN_list: list of access identifiers for this share
            """            
            data = {
                "accessIdentifiers": ARN_list.__str__().replace(" ", "").replace(
                    "\'", "\"")
            }
            params = {
                "_data": "routes/__auth/shares/$shareId/destination/edit"
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
            """
            This class represents a delivery, and should only be acquired by the user through calling get_delivery or create_delivery on a Share
            """
            def __init__(self, delivery_id, share_id, session, base_url):
                self.delivery_id = delivery_id
                self.share_id = share_id
                self.s = session
                self.base_url = base_url

            def __str__(self):
                return self.__repr__()
                        
            def __repr__(self):
                return "Delivery(" + self.delivery_id + ")"

            def deliver_delivery(self):
                """Delivers this Delivery
                
                :calls: `POST /shares/{share_id}`
                """                
                data = {
                    "deliverDeliveryId": self.delivery_id
                }
                params = {
                    "_data": "routes/__auth/shares/$shareId"
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