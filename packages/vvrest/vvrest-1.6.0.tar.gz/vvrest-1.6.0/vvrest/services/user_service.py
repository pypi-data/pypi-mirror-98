import requests
from ..constants import USERS_URL, WEB_TOKEN_URL, SITE_ID_URL, JWT_URL


class UserService:
    def __init__(self, vault):
        self.vault = vault

    def get_users(self, query=''):
        """
        get all users or search by query
        :param query: string, default: empty string, example: "userId='test@test.com'"
        :return: dict
        """
        request_url = self.vault.base_url + USERS_URL
        if query:
            request_url += '?q=' + query

        headers = self.vault.get_auth_headers()
        resp = requests.get(request_url, headers=headers).json()
        return resp

    def get_user(self, user_id):
        """
        get a single user
        :param user_id: string uuid4
        :return: dict
        """
        endpoint = USERS_URL + '/' + user_id
        request_url = self.vault.base_url + endpoint
        headers = self.vault.get_auth_headers()
        resp = requests.get(request_url, headers=headers).json()

        return resp

    def get_user_web_token(self, user_id):
        """
        get a users webToken by userId
        :param user_id: string uuid4
        :return: dict
        """
        endpoint = USERS_URL + '/' + user_id + '/' + WEB_TOKEN_URL
        request_url = self.vault.base_url + endpoint
        headers = self.vault.get_auth_headers()
        resp = requests.get(request_url, headers=headers).json()

        return resp

    def create_user(self, site_id, user_id, first_name, last_name, email, password, must_change_password=False,
                    send_email=False, password_never_expires=True):
        """
        create a new user
        :param site_id: string uuid4
        :param user_id: string uuid4
        :param first_name: string
        :param last_name: string
        :param email: string
        :param password: string
        :param must_change_password: bool, default False
        :param send_email: bool, default False
        :param password_never_expires: bool, default True
        :return: dict
        """
        endpoint = USERS_URL + SITE_ID_URL + site_id
        request_url = self.vault.base_url + endpoint
        headers = self.vault.get_auth_headers()

        payload = {
            'userId': user_id,
            'firstName': first_name,
            'lastName': last_name,
            'emailAddress': email,
            'password': password,
            'mustChangePassword': must_change_password,
            'sendEmail': send_email,
            'passwordNeverExpires': password_never_expires
        }

        resp = requests.post(request_url, headers=headers, data=payload).json()

        return resp

    def update_user(self, user_id, fields_dict):
        """
        update a user
        :param user_id: string uuid4
        :param fields_dict: dict, example: {'enabled': True, 'lastName': 'new name'}
        :return: dict
        """
        endpoint = USERS_URL + '/' + user_id
        request_url = self.vault.base_url + endpoint
        headers = self.vault.get_auth_headers()
        resp = requests.put(request_url, headers=headers, data=fields_dict).json()

        return resp

    def get_user_jwt(self):
        """
        get a users JWT by userId
        refreshes a users JWT if JWT is passed into Vault object
        :return: dict
        """
        endpoint = USERS_URL + '/' + JWT_URL
        request_url = self.vault.base_url + endpoint
        headers = self.vault.get_auth_headers()
        resp = requests.get(request_url, headers=headers).json()

        return resp
