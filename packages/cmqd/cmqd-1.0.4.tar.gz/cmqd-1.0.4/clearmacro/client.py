import re
import json
import requests
from clearmacro.errors import ResponseError
from clearmacro.configuration import Configuration
from clearmacro.events import Events
from clearmacro.operations import Operations
from clearmacro.version import VERSION
import jwt
import time


class Client(Events, Operations):
    configuration = None

    _user_agent = 'ClearMacro/python@{}'.format(VERSION)
    user_agent = "ClearMacro/python@{}".format(VERSION)

    def __init__(self, **configuration_overrides):
        """
        Instantiates a client to connect to the ClearMacro API.

        Args:
            **configuration_overrides: A configuration structure providing the API host, username and password.

        Examples:
            >>> config = {'url': 'https://api.clearmacro.com','username': 'abc', 'password':'123'}
            >>> client = Client(**config)
        """
        super().__init__()
        self.configuration = Configuration(**configuration_overrides)
        self._on("request", lambda req: self.configuration.logger.debug('Request: %s', req))
        self._on("response", lambda res: self.configuration.logger.debug('Request: %s', res))
        self._on("error", lambda err: self.configuration.logger.error(err))
        self._inputErrorMessage = 'Invalid input.'

        # refresh credentials on the Client instance
        self._refresh_credentials()

    def _is_access_token_expired(self):
        claims = jwt.decode(self.configuration.credentials['access_token'], verify=False)
        exp = int(claims['exp'])
        now = time.time()
        if now < exp:
            return False
        else:
            return True

    def _refresh_credentials(self):
        self.configuration.credentials = self._login(self.configuration.username, self.configuration.password)

    def _request(self, path, method, **params):
        if path != '/api/auth/login' and self._is_access_token_expired():
            # not attempting to login and the token has expired
            self._refresh_credentials()

        url = self._build_request_url(path)
        request_params = {**params, **self.configuration.request_params()}
        self._emit('request', {'url': url, **request_params})
        response = self._call_request(url, method, request_params)
        data = response.json()
        self._emit('response', data)
        self.configuration.LOG.debug(f'Call made to: {url}')
        if "x-permissions-token" in response.headers:
            self.configuration.credentials['permissions_token'] = response.headers.get('x-permissions-token')
        return data

    def _call_request(self, url, method, params={}):
        try:
            request = getattr(requests, method)
            response = request(url, **params)
            if response.status_code == requests.codes.ok:
                return response
            try:
                raise ResponseError(**response.json(), type="message")
            except json.decoder.JSONDecodeError:
                raise ResponseError(response, type="network-error")
        except requests.exceptions.Timeout:
            raise ResponseError("Connection timed out", type="timeout")
        except requests.exceptions.RequestException as e:
            raise ResponseError(str(e), type="liberror")
        except ResponseError as ex:
            raise ResponseError(ex, type="message")

    def _build_request_url(self, path):
        request_url = self.configuration.url + path
        safe_request_url = re.sub(r"(?<!:)\/\/", "/", request_url)
        return safe_request_url
