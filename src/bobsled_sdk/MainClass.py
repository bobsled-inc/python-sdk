import requests

from bobsled_sdk.utils import flatten, handle_errors
from . import BobsledException

class BobsledClient:
    """
    This is the main class you instantiate to access Bobsled. 
    """
    
    def __init__(self, credentials, base_url = "http://127.0.0.1:3000"):
        self.credentials = credentials
        self.base_url = base_url.strip("/")
        self.s = requests.Session()
        headers = {
            "User-Agent": "Bobsled-Python-SDK/Python",
        }
        self.s.headers.update(headers)
        
        params = {
            "_data": "routes/__unauth/signin-with-password"
        }
        
        r = self.s.post(
            base_url + "/signin-with-password",
            data=self.credentials,
            params=params)
        if r.status_code != 204:
            handle_errors(r)

    def list_shares(self):
        """Returns a list of share_ids that can be used with get_share

        :calls: `GET /shares`
        :return: a list of share_ids
        """        
        params = {
            "_data": "routes/__auth/shares"
        }
        
        r = self.s.get(
            self.base_url +"/shares",
            params=params
        )
        if r.status_code != 200:
            handle_errors(r)
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
            "_data": "routes/__auth/shares"
        }
        
        r = self.s.post(self.base_url +
                        "/shares",
                        params=params)
        if r.status_code != 204:
            handle_errors(r)
        header_str = r.headers["x-remix-redirect"]
        share_id = header_str[8:].split("/")[0]
        return self.Share(share_id, self.s, self.base_url)


    class Share:
        """
        This class represents a share, and should only be acquired by the user through calling get_share or create_share on a BobsledClient
        """
        def __init__(self, share_id, session, base_url):
            self.share_id = share_id
            self.s = session
            self.base_url = base_url
            
            params = {"_data": "routes/__auth/shares.$shareId/$role"}
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id + "/provider",
                params=params
            )
            
            if r.status_code != 200:
                handle_errors(r)

        def get_id(self):
            return self.share_id
        
        def get_share_information(self):
            """Retrieves and returns full information on the share
            
            :calls: `GET /shares/{share_id}`
            :return: Dictionary containing full information on the share
            """            
            params = {"_data": "routes/__auth/shares.$shareId/$role"}
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id + "/provider",
                params=params
            )
            
            if r.status_code != 200:
                handle_errors(r)
            
            return r.json()
        
        def archive(self):
            """Archives current share
            
            :calls; `POST /shares/{share_id}`
            """            
            
            params = {
                "_data": "routes/__auth/shares.$shareId/$role"
            }
            
            data = {
                "actionType": "archive"
            }
            
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id + "/provider",
                params=params,
                data=data
            )
            
            if r.status_code != 204:
                handle_errors(r)
                
        def restore(self):
            """Restores this archived share
            
            :calls: `POST /shares/{share_id}`
            """            
            params = {
                "_data": "routes/__auth/shares.archived.$archivedShareId"
            }
            r = self.s.post(
                self.base_url + "/shares/archived/" + self.share_id,
                params = params
            )
            
            if r.status_code != 204:
                handle_errors(r)
        
        # WIP
        def update(self, params):
            """Updates share according to parameters provided in params
            
            params = {
                name,
                description,
                locationId, # this is for source location
                cloud,
                region,
                consumers
            }
            
            :param params: dictionary containing several optional fields
            """            
        
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id + 
                "/driver",
                data=params
            )
            
            if r.status_code != 204:
                handle_errors(r)

        def set_overview(self, name, description):
            """Sets overview text of the share
            
            :calls: `GET /shares/{share_id}/overview`
            """
        
            data = {
                "name": name,
                "description": description
            }
            
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/overview"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/overview",
                data=data,
                params=params)
            if r.status_code != 204:
                handle_errors(r)

        def get_source_locations(self):
            """Retrieves and returns locations that can be used in set_source_location
            
            :calls: `GET /shares/{share_id}/source`
            :return: list of locations 
            """
            
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/source"
            }
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/provider/source",
                params=params)
            if r.status_code != 200:
                handle_errors(r)
            json_locations = r.json()['locations']
            return json_locations

        def set_source_location(self, location_id):
            """Set the source of the share to location_id

            :calls: `POST /shares/{share_id}/source`
            :param location_id: unique identifier of a source container
            """            
            data = {"locationIdJs": location_id,
                    "locationId": location_id,
                    }
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/source"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/source",
                data=data,
                params=params)
            if r.status_code != 204:
                handle_errors(r)

        def get_destination_locations(self):
            """Get destination locations that can be used in set_destination_location

            :calls: `GET /shares/{share_id}/destination/new`
            :return: something, a list or dictionary of locations, undecided
            """            
            
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/destination/new"
            }
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/provider/destination/new",
                params=params
            )
            if r.status_code != 200:
                handle_errors(r)
            return r.json()

        def set_destination_location(self, cloud, region):
            """Sets destination location of this share to given cloud and location_id (region?)

            :calls: `POST /shares/{share_id}/destination/new`
            :param cloud: cloud provider (e.g. AWS)
            :param region: id of a region inside the cloud
            """         
               
            data = {"cloud": cloud, "region": region}
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/destination/new"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/destination/new",
                data=data,
                params=params)
            if r.status_code != 204:
                handle_errors(r)

        def get_all_files(self, path="/", time=0):
            """Returns flattened contents of all files that were last modified after time in source location

            :calls: `GET /shares/{share_id}/loadCloudData`
            :param time: folder path (with format `/top_level_folder/another_folder/`) and UNIX timestamp in seconds
            :return: list of file paths, total size of files
            """            
            params = {
                "_data": "routes/__auth/shares.$shareId/loadCloudData"
            }
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/loadCloudData",
                params=params)
            if r.status_code != 200:
                handle_errors(r)
            folderContents = r.json()['folderContents']

            prefix = self.get_share_information()["share"]["sourceLocation"]["url"]
            
            if path[-1] != "/":
                raise BobsledException.BobsledException(status = -1, data = "Invalid input (must end in a folder)")
            
            # Navigating into the right folder to run flatten on
            l = 0
            r = 0
            length = len(path)
            folder_stack = []
            while l < length and r < length:
                if path[r] == "/":
                    folder_stack.append(path[l: r+1])
                    l = r + 1
                    r = r + 1
                r += 1
                
            folder_stack.reverse()
            if folder_stack[-1] == "/":
                folder_stack[-1] = "root"
            
            while folder_stack:
                found = False
                for obj in folderContents:
                    if obj['name'] == folder_stack[-1]:
                        folderContents = obj['content']
                        folder_stack.pop()
                        found = True
                        break
                if not found:
                    raise BobsledException.BobsledException(status = -1, data = "Path doesn't exist")
            
            return flatten(folderContents, prefix, time)
        
        def get_source_contents(self):
            """Returns folder structure of source location and prefix

            :calls: `GET /shares/{share_id}/loadCloudData`
            :return: prefix and dictionary representing folder structure at source location
            """            
            params = {
                "_data": "routes/__auth/shares.$shareId/loadCloudData"
            }
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/loadCloudData",
                params=params)
            if r.status_code != 200:
                handle_errors(r)
            folderContents = r.json()['folderContents']
            
            prefix = self.get_share_information()["share"]["sourceLocation"]["url"]
            
            return prefix, folderContents

        def get_deliveries(self):
            """Returns the list of deliveries of this share

            :calls: `GET /shares/{share_id}`
            :return: list of deliveries
            """            
            
            share_info = self.get_share_information()
            return share_info["deliveries"]

        def create_delivery(self, selection, size = 1000, overwriteMode = False):
            """Creates and returns a Delivery object given selection of file paths

            :calls: `POST /shares/{share_id}/delivery`
            :param selection: file paths for files in the source container to be included in this delivery
            :param size: total size of files in this delivery
            :param overwriteMode: boolean indicating whether overwriteMode is on (True) or off (False)
            """            

            data = {
                "sharedFiles": selection.__str__().replace("\', \'", "\',\'").replace(
                    "\'", "\""), # we have to fit specific format
                "totalSize": size, # placeholder
                "overwriteMode": str(overwriteMode).lower()
            }
            
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/delivery",
                data=data,
                allow_redirects=False)
            
            if r.status_code != 302:
                handle_errors(r)
            
            return self.Delivery(r.text, self)
        
        def get_delivery(self, delivery_id):
            """Returns the Delivery object given the delivery_id

            :param delivery_id: unique id of the delivery
            :return: Delivery object
            """            
            return self.Delivery(delivery_id, self)

        def get_team(self):
            """Returns team members

            :calls: `GET /shares/{share_id}/team`
            :return: dictionary representing team members
            """            
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/team"
            }
            
            r = self.s.get(
                self.base_url + "/shares/" + self.share_id +
                "/provider/team",
                params=params)
            if r.status_code != 200:
                handle_errors(r)
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
                "_data": "routes/__auth/shares.$shareId/$role/team"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/team",
                data=data,
                params=params)
            if r.status_code != 200:
                handle_errors(r)
                
        def add_consumers(self, consumer_email_list):
            """Adds all emails provided to consumers

            :calls: `POST /shares/{share_id}/team`
            :param consumer_email_list: list of email addresses of the consumers to be added
            """            
            data = {
                "role": "consumer",
                "actionType": "addUserToShare"
            }
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/team"
            }
            for email in consumer_email_list:
                data["email"] = email
                r = self.s.post(
                    self.base_url + "/shares/" + self.share_id +
                    "/provider/team",
                    data=data,
                    params=params)
                if r.status_code != 200:
                    handle_errors(r)

        # Currently this takes id (not email), which can be unintuitive to the user
        def send_invitation(self, id):
            """Sends the invitation to added member

            :param id: id of the member (not email)
            """            
            data = {
                "memberToReceiveInvitationId": id,
                "actionType": "sendEmail"
            }
            
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/team"
            }
            
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/team",
                data=data,
                params=params
            )
            if r.status_code != 200:
                handle_errors(r)

        def add_access_identifiers(self, ARN_list):
            """Edit access identifiers of this share

            :param ARN_list: list of access identifiers for this share
            """            
            data = {
                "accessIdentifiers": ARN_list
            }
            params = {
                "_data": "routes/__auth/shares.$shareId/$role/destination/edit"
            }
            r = self.s.post(
                self.base_url + "/shares/" + self.share_id +
                "/provider/destination/edit",
                data=data)
            if r.status_code != 204 and r.status_code != 200:
                handle_errors(r)
                
        def remove_access_identifiers(self, ARN_list):
            """Remove access identifiers of this share

            :param ARN_list: list of access identifiers for this share
            """            
            return
            # we want to change ARNs into their ids
            # ARN_id_list = []
            
            
            # data = {
            #     "accessIdentifiers": ARN_list
            # }
            # params = {
            #     "_data": "routes/__auth/shares.$shareId/$role/destination/edit"
            # }
            # r = self.s.post(
            #     self.base_url + "/shares/" + self.share_id +
            #     "/provider/destination/edit",
            #     data=data)
            # if r.status_code != 204 and r.status_code != 200:
            #     handle_errors(r)

        class Delivery:
            """
            This class represents a delivery, and should only be acquired by the user through calling get_delivery or create_delivery on a Share
            """
            def __init__(self, delivery_id, share):
                self.delivery_id = delivery_id
                self.share = share
                self.share_id = share.share_id
                self.s = share.s
                self.base_url = share.base_url

            def __str__(self):
                return self.__repr__()
                        
            def __repr__(self):
                return "Delivery(" + self.delivery_id + ")"

            def deliver_delivery(self):
                """Delivers this Delivery
                
                :calls: `POST /shares/{share_id}`
                """                
                data = {
                    "deliverDeliveryId": self.delivery_id,
                    "actionType": "deliverDelivery"
                }
                params = {
                    "_data": "routes/__auth/shares.$shareId/$role"
                }
                r = self.s.post(
                    self.base_url + "/shares/" + self.share_id + "/provider",
                    data=data,
                    params=params)
                if not (200 <= r.status_code < 300):
                    handle_errors(r)
            
            def status(self):
                """Returns the current status of the delivery

                :return: a string representing the current state of the delivery: "published", "delivering", "delivered", "invalid"
                """                
                share_info = self.share.get_share_information()
                for delivery in share_info["deliveries"]:
                    if delivery["id"] == self.delivery_id:
                        return delivery["state"]
                return "invalid"
                
            def access(self):
                """Returns the URL to access this delivery

                :calls: `GET /shares/{share_id}/deliveries/{delivery_id}/access`
                :return: URL where deliveries can be accessed
                """                
                
                params = {
                    "_data": "routes/__auth/shares.$shareId/$role/deliveries/$deliveryId/access"
                }
                
                r = self.s.get(
                    self.base_url + "/shares/" + self.share_id + "/provider/deliveries/" + self.delivery_id + "/access",
                    params=params)
                
                if r.status_code != 200:
                    handle_errors(r)
                
                url = r.json()["delivery"]["url"]
                return url