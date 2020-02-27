"""

Liana REST API client

Copyright Liana Technologies Ltd 2018

"""

import json
import hashlib
import hmac
import requests
import time

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

    def call(self, path, params=[], method='POST'):
        """ Perform API request and return the API result"""
        request_function = getattr(requests, method.lower())
        self._set_request_data(path, params, method)

        self._response = request_function(
            self._api_url + self._full_path,
            headers=self._get_headers(),
            data=self._json_string
        )

        self._response_body = self._response.text;

        if (self._response.status_code >= 400):
            raise APIException(
                'API response with status code ' +str(self._response.status_code)
             )

        try:
            data = json.loads(self._response_body);
        except ValueError: # Python 2.x
            raise APIException('API did not return a valid json string')
        except json.decoder.JSONDecodeError: # Python 3.5+
            raise APIException('API did not return a valid json string')

        return data

    def get_http_response(self):
        """ Returns the raw response object of last performed API request """
        return self._response



    """ INTERNAL METHODS FOLLOW """

    def _get_new_timestamp(self):
        """ Returns a fresh timestamp in proper format """
        return time.strftime('%Y-%m-%dT%H:%M:%S%z')

    def _get_hash(self):
        """ Form and return the parameters hash for the API request """
        md5 = hashlib.md5()
        md5.update(self._json_string.encode('utf-8'))
        return md5.hexdigest()


    def _get_message(self):
        """ Return the message in the format which is used to create signature of the request """
        message = "\n".join([
            self._method,
            self._get_hash(),
            self._content_type,
            self._timestamp,
            self._json_string,
            self._full_path
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


    def _set_request_data(self, path, params, method):
        """ Set API request data """
        self._full_path = '/api/v' + str(self._api_version) + '/' + path
        self._json_string = json.dumps(params)
        if method == 'GET':
			self._json_string = ''
        self._timestamp = self._get_new_timestamp()
        self._method = method

