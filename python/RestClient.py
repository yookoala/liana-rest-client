"""

Liana REST API client

Copyright Liana Technologies Ltd 2018

"""

import json
import hashlib
import hmac
import requests
from datetime import datetime

class APIException(Exception):
    pass

class RestClient:
    def __init__(self, user_id, api_secret, api_url, api_version, api_realm):
        self._response = None
        self._user_id = user_id
        self._api_secret = api_secret
        self._api_url = api_url
        self._api_realm = api_realm
        self._api_version = api_version
        self._content_type = 'application/json'

    def call(self, method, params=[]):
        """ Perform API request and return the API result"""
        self._set_request_data(method, params)

        self._response = requests.post(
            self._api_url + self._full_method,
            headers=self._get_headers(),
            data=self._json_string
        )

        self._response_body = self._response.text;

        if self._response.status_code != 200:
            raise APIException(
                'API response with status code ' + str(self._response.status_code) + ' instead of OK (200)'
            )

        try:
            data = json.loads(self._response_body);
        except ValueError: # Python 2.x
            raise APIException('API did not return a valid json string')
        except json.decoder.JSONDecodeError: # Python 3.5+
            raise APIException('API did not return a valid json string')

        if not data['succeed']:
            raise APIException(data['message'])

        return data['result']

    def get_http_response(self):
        """ Returns the raw response object of last performed API request """
        return self._response



    """ INTERNAL METHODS FOLLOW """

    def _get_new_timestamp(self):
        """ Returns a fresh timestamp in proper format """
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    def _get_hash(self):
        """ Form and return the parameters hash for the API request """
        md5 = hashlib.md5()
        md5.update(self._json_string.encode('utf-8'))
        return md5.hexdigest()


    def _get_message(self):
        """ Return the message in the format which is used to create signature of the request """
        message = "\n".join([
            'POST',
            self._get_hash(),
            self._content_type,
            self._timestamp,
            self._json_string,
            self._full_method
        ])
        return message.encode('utf-8')


    def _get_signature(self):
        """ Get signature for the API request """
        return hmac.new(
            self._api_secret.encode('utf-8'),
            self._get_message(),
            hashlib.sha256
        ).hexdigest()


    def _get_headers(self):
        """ Get headers for the API HTTP request """
        return {
            'Content-Type': self._content_type,
            'Content-MD5': self._get_hash(),
            'Date': self._timestamp,
            'Authorization': self._api_realm + ' ' + str(self._user_id) + ':' + self._get_signature(),
        }


    def _set_request_data(self, method, params):
        """ Set API request data """
        self._full_method = '/api/v' + str(self._api_version) + '/' + method
        self._json_string = json.dumps(params)
        self._timestamp = self._get_new_timestamp()

