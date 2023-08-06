"""
    Geostreams Client
    ~~~
    This module contains a basic client to interact with the Geostreams API.
"""


from builtins import object
import json
import logging
import time
from typing import Union, Tuple

import requests
from requests.exceptions import RequestException


class GeostreamsClient(object):
    """
    Client to Geostreams API to store connection information.

    The `path` parameter used by many of the methods in this class call a specific path relative to the host + "api".
    For example passing in "/version" for host "https://seagrant-dev.ncsa.illinois.edu/" will call
    "https://seagrant-dev.ncsa.illinois.edu/api/version". Make sure to include the slash at the beginning of
    the fragment.
    """
    logger = logging.getLogger(__name__)
    api_fragment = "/api"
    max_retries = 10
    call_timeout = 5

    def __init__(self, *args, **kwargs):
        """
        Create an instance of `GeostreamsClient`.

        :param string host: The root host url of the specific geostreaming API we are connecting to.
        :param string key: The API key used to write to the API. Set this or `username`/`password` below.
        :param string username: HTTP Basic Authentication username.
        :param string password: HTTP Basic Authentication password.
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous exception
            while handling a request
         """
        self.host = kwargs.get('host')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.user = {'identifier': self.username, 'password': self.password}

        login_url = self.host + "/api/authenticate"
        r = requests.post(login_url, json=self.user, headers={'Content-Type': 'application/json'}, timeout=(60, 120))
        try:
            r.raise_for_status()
            self.headers = {"x-auth-token": r.headers["x-auth-token"], "Content-Encoding": "application/json"}
        except RequestException as e:
            logging.exception(f"Could not authenticate.\n {e}")
            raise e

    def version(self):
        """Return Geostreams version info."""
        url = self.host + self.api_fragment + "/version"
        self.logger.debug("GET %s", url)
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            try:
                json = r.json()
                self.logger.debug("Version: %s", json)
                return json
            except ValueError:
                self.logger.error(f"GET {url}. Could not parse JSON. Status {r.status_code}.")
                r.raise_for_status()
        else:
            r.raise_for_status()

    def get_json(self, path, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP GET against `path`. This version returns a JSON object.

        :param path: Endpoint path relative to Geostreams api.
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: JSON from body of response
        :rtype: JSON
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path
        r = requests.get(url, headers=self.headers, timeout=timeout)
        try:
            r.raise_for_status()
            return r.json()
        except RequestException as e:
            logging.exception(f"Error calling GET url {url}: {e}")
            raise e

    def get(self, path, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP GET against `path`. This version returns a `requests.Response` object.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path
        try:
            return requests.get(url, headers=self.headers, timeout=timeout)
        except requests.exceptions.ConnectionError as e:
            raise e
        except RequestException as e:
            logging.exception(f"Error calling GET url {url}: {e}")
            raise e

    def get_retry(self, path, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP GET against `path`. This version returns a `requests.Response` object. Useful in case of temporary
        network issues.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path
        for x in range(self.max_retries):
            r = requests.get(url, headers=self.headers, timeout=timeout)
            if 200 <= r.status_code < 300:
                return r.json()
            else:
                logging.warning(f"Error calling GET url {url}")
                logging.warning(f"Waiting {self.call_timeout} seconds and will try again")
                time.sleep(self.call_timeout)
        try:
            r.raise_for_status()
        except RequestException as e:
            logging.exception(f"Error calling GET url {url}: {e}")
            raise e

    def post(self, path, content, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP POST against `path` with `content` in body.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :param content: Content to send as the body of the request.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path

        try:
            k = requests.post(url, json=content, headers=self.headers, timeout=timeout)
            return k
        except RequestException as e:
            self.logger.error(f"POST {url}: {e}")
            raise e

    def put(self, path, content, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP POST against `path` with `content` in body.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :param content: Content to send as the body of the request.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path

        try:
            k = requests.put(url, json=content, headers=self.headers, timeout=timeout)
            return k
        except RequestException as e:
            self.logger.error(f"PUT {url}: {e}")
            raise e

    def post_file(self, path, filename, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP POST against `path` with `content` in body. Header with content-type is not required.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :param filename: Content to send as the body of the request.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """

        url = self.host + self.api_fragment + path

        try:
            return requests.post(url, files={"File": open(filename, 'rb')},
                                 headers=self.headers, timeout=timeout)
        except RequestException as e:
            self.logger.error(f"POST {url}: {e}")
            raise e

    def post_retry(self, path, content, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP POST against `path` with `content` in body. Retry up to a certain number of times if necessary. Useful
        in case of temporary network issues.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :param content: Content to send as the body of the request.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path
        for i in range(self.max_retries):
            r = requests.post(url, data=json.dumps(content), headers=self.headers, timeout=timeout)
            if 200 <= r.status_code < 300:
                return r.json()
            else:
                logging.warning(f"Error calling POST url {url}")
                logging.warning(f"Waiting {self.call_timeout} seconds and will try again")
                time.sleep(self.call_timeout)
        try:
            r.raise_for_status()
        except RequestException as e:
            logging.exception(f"Error calling POST url {url}: {e}")
            raise e

    def delete(self, path, timeout: Union[int, Tuple[int, int]] = (120, 600)):
        """
        Call HTTP DELETE against `path`.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path
        r = requests.delete(url, headers=self.headers, timeout=timeout)
        try:
            r.raise_for_status()
            return r
        except RequestException as e:
            self.logger.error(f"DELETE {url}: {e}")
            raise e

    def delete_retry(self, path, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Call HTTP DELETE against `path`. Retry up to a certain number of times if necessary. Useful in case of temporary
        network issues.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :param path: Endpoint path relative to Geostreams api.
        :return: Full response object so that we can check status on it and then retrieve the JSON body.
        :rtype: `requests.Response`
        :raises:
            requests.exceptions.RequestsException: an http, connection, timeout, read timeout, or an ambiguous
            exception while handling a request
            ValueError: if timeout is a wrong tuple
        """
        url = self.host + self.api_fragment + path
        for x in range(self.max_retries):
            r = requests.delete(url, headers=self.headers, timeout=timeout)
            if 200 <= r.status_code < 300:
                return r.json()
            else:
                logging.warning(f"Error calling DELETE url {url}")
                logging.warning(f"Waiting %i seconds and will try again" % self.call_timeout)
                time.sleep(self.call_timeout)
        try:
            r.raise_for_status()
        except RequestException as e:
            logging.exception(f"Error calling DELETE url {url}: {e}")
            raise e
