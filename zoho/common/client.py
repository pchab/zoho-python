# coding: utf8
import requests
from urllib.parse import urlencode
from zoho.common.exceptions import InvalidModuleError, NoPermissionError, InvalidDataError, MandatoryFieldNotFoundError


class Client(object):
    AUTHORIZE_URL = 'https://accounts.zoho.com/oauth/v2/auth'
    REQUEST_TOKEN_URL = 'https://accounts.zoho.com/oauth/v2/token'
    REFRESH_TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"

    def __init__(self, client_id, client_secret, redirect_uri, scope, access_type, refresh_token=None):
        self.code = None
        self.scope = scope
        self.access_type = access_type
        self.client_id = client_id
        self._refresh_token = refresh_token
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.access_token = None

    def get_authorization_url(self):
        """

        :return:
        """
        params = {'scope': ','.join(self.scope), 'client_id': self.client_id, 'access_type': 'offline',
                  'redirect_uri': self.redirect_uri, 'response_type': 'code', 'prompt':'consent'}
        url = self.AUTHORIZE_URL + '?' + urlencode(params)
        return url

    def exchange_code(self, code):
        """

        :param code:
        :return:
        """
        params = {'code': code, 'client_id': self.client_id, 'client_secret': self.client_secret,
                  'redirect_uri': self.redirect_uri, 'grant_type': 'authorization_code'}
        url = self.REQUEST_TOKEN_URL + '?' + urlencode(params)
        return self._post(url)

    def refresh_token(self):
        """

        :return:
        """
        params = {'refresh_token': self._refresh_token, 'client_id': self.client_id,
                  'client_secret': self.client_secret, 'grant_type': 'refresh_token'}
        url = self.REFRESH_TOKEN_URL + '?' + urlencode(params)
        response = self._post(url)
        return response

    def set_access_token(self, token):
        """

        :param token:
        :return:
        """
        if isinstance(token, dict):
            self.access_token = token['access_token']
            if 'refresh_token' in token:
                self._refresh_token = token['refresh_token']
        else:
            self.access_token = token

    def _get(self, endpoint, params=None):
        headers = {'Authorization': 'Zoho-oauthtoken {0}'.format(self.access_token), }
        response = requests.get(endpoint, params=params, headers=headers)
        return self._parse(response, method='get')

    def _post(self, endpoint, params=None, data=None):
        headers = {'Authorization': 'Zoho-oauthtoken {0}'.format(self.access_token), }
        response = requests.post(endpoint, params=params, json=data, headers=headers)
        return self._parse(response, method='post')

    def _put(self, endpoint, params=None, data=None):
        headers = {'Authorization': 'Zoho-oauthtoken {0}'.format(self.access_token), }
        response = requests.put(endpoint, params=params, json=data, headers=headers)
        return self._parse(response, method='put')

    def _patch(self, endpoint, params=None, data=None):
        headers = {'Authorization': 'Zoho-oauthtoken {0}'.format(self.access_token), }
        response = requests.patch(endpoint, params=params, json=data, headers=headers)
        return self._parse(response, method='patch')

    def _delete(self, endpoint, params=None):
        headers = {'Authorization': 'Zoho-oauthtoken {0}'.format(self.access_token), }
        response = requests.delete(endpoint, params=params, headers=headers)
        return self._parse(response, method='delete')

    def _parse(self, response, method=None):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201):
            return r
        if status_code == 204:
            return None
        message = None
        try:
            if 'message' in r:
                message = r['message']
        except Exception:
            message = 'No error message.'
        if status_code == 400:
            raise InvalidModuleError(message)
        if status_code == 401:
            raise NoPermissionError(status_code)
        if status_code == 201:
            raise MandatoryFieldNotFoundError(message)
        elif status_code == 202:
            raise InvalidDataError(message)
        elif status_code == 400:
            raise InvalidDataError(message)
