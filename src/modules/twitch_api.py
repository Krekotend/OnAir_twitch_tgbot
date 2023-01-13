import requests

"""This module makes a request to Twitch and returns 
the main parameters about the stream (id, status, etc.)"""


class Streaminfo:

    def __init__(self, client_id : str, client_secret: str, user_name: str) :
        self.client_id = client_id  # your id
        self.client_secret = client_secret  # your secret key
        self.user_name = user_name  # channel name
        self._user_id = None

    @property
    def access_token(self):

        """Gets the access token needed for the main request """

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        response = requests.post("https://id.twitch.tv/oauth2/token", params=params)

        if response.json() == {'status': 400, 'message': 'invalid client'} or \
                response.json() == {'status': 403, 'message': 'invalid client secret'}:
            raise InvalidClient(response.json()['message'])

        access_token = response.json()["access_token"]

        return access_token

    @property
    def user_id(self):

        """Gets the user id needed for the main request """

        if self._user_id is None:
            params = {"login": self.user_name}

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Client-Id": self.client_id}

            response = requests.get("https://api.twitch.tv/helix/users", params=params, headers=headers)

            if len(response.json()['data']) == 0:
                raise InvalidUser("Invalid user")

            self._user_id = response.json()["data"][0]['id']

            return self._user_id
        return self._user_id

    def stream(self):

        """Main request returns a list with the main parameters about the stream"""

        params = {"user_id": self.user_id}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id}

        response = requests.get("https://api.twitch.tv/helix/streams",
                                params=params, headers=headers)

        if response.json() == {'error': 'Unauthorized', 'status': 401, 'message': 'OAuth token is missing'} or \
                response.json() == {'error': 'Unauthorized', 'status': 401, 'message': 'Invalid OAuth token'}:
            raise InvalidOAuthToken(response.json()['message'])

        if response.json() == {'error': 'Unauthorized', 'status': 401,
                               'message': 'Client ID and OAuth token do not match'}:
            raise ValuesNotMatching(response.json()['message'])

        if response.json() == {'data': [], 'pagination': {}}:
            return [{'type': 'Offline'}]  # "The user is not broadcasting"

        data = response.json()["data"]

        return data


class InvalidUser(Exception):
    pass


class InvalidClient(Exception):
    pass


class InvalidOAuthToken(Exception):
    pass


class ValuesNotMatching(Exception):
    pass


if __name__ == "__main__":
    Unit = Streaminfo('<"client_id">, <"client_secret">, <"user_name">')
    print(Unit.stream())  # main answer
