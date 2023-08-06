"""
    Geostreams Streams API
"""

from builtins import range
from builtins import object
import logging

import json
from typing import Union, Tuple

from requests.exceptions import RequestException

from pygeostreams.client import GeostreamsClient


class StreamsApi(object):
    """
        API to manage the REST CRUD endpoints for Streams.
    """
    def __init__(self, client=None, host=None, username=None, password=None):
        """Set client if provided otherwise create new one"""
        if client:
            self.api_client = client
        else:
            self.client = GeostreamsClient(host=host, username=username, password=password)

    def streams_get(self, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get the list of all available streams.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Full list of streams.
        :rtype: `requests.Response`
        """
        logging.debug("Getting all streams")
        try:
            return self.client.get("/streams", timeout)
        except RequestException as e:
            logging.error(f"Error retrieving stream list: {e}")
            raise e

    def streams_get_by_id(self, stream_id,
                          timeout: Union[int, Tuple[int, int]] = (125, 605)):
        logging.debug(f"Getting stream with id {stream_id}")
        try:
            return self.client.get("/streams/%s" % stream_id, timeout)
        except RequestException as e:
            logging.error(f"Error retrieving stream with id {stream_id}: {e}")
            raise e

    def stream_get_by_name_json(self, stream_name,
                                timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get a specific stream by id.

        :param stream_name:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: stream object as JSON.
        :rtype: `requests.Response`
        """
        logging.debug(f"Getting stream {stream_name}")
        try:
            stream = self.client.get("/streams?stream_name=" + stream_name, timeout).json()
            if 'status' in stream and stream['status'] == "No data found" or not stream["streams"]:
                return None
            else:
                return stream
        except RequestException as e:
            logging.error(f"Error retrieving stream with name {stream_name}: {e}")
            raise e

    def stream_post(self, stream, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Create stream.

        :return: stream json.
        :rtype: `requests.Response`
        """
        logging.debug("Adding stream")

        try:
            return self.client.post("/streams", stream, timeout)
        except RequestException as e:
            logging.error(f"Error retrieving streams: {e}")
            raise e

    def stream_post_json(self, stream, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Create stream.

        :param stream:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: stream json.
        :rtype: `requests.Response`
        """
        logging.debug("Adding or getting stream")
        try:
            stream_from_geostreams = self.stream_get_by_name_json(stream['name'], timeout)

            if stream_from_geostreams is None:
                logging.info(f"Creating stream with name: {stream['name']}")
                result = self.client.post("/streams", stream, timeout)
                if result.status_code != 200:
                    logging.info("Error posting stream")
                stream_from_geostreams = self.stream_get_by_name_json(stream['name'], timeout)

            logging.info(f"Found stream {stream['name']}")
            return stream_from_geostreams["streams"][0]
        except RequestException as e:
            logging.error(f"Could not post stream: {e}")
            raise e

    def stream_delete(self, stream_id, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Delete a specific stream by id.

        :param stream_id:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: If successful or not.
        :rtype: `requests.Response`
        """
        logging.debug(f"Deleting stream {stream_id}")
        try:
            return self.client.delete("/streams/%s" % stream_id, timeout)
        except RequestException as e:
            logging.error(f"Error deleting stream {stream_id}: {e}")
            raise e

    def stream_create_json_from_sensor(self, sensor):
        """
        Create stream from sensor. Note: It does not post the stream to the API

        :param: sensor
        :return: stream Json object
        """

        stream = {
            "sensor_id": sensor['id'],
            "name": sensor['name'],
            "type": sensor['geoType'],
            "geometry": sensor['geometry'],
            "properties": sensor['properties']
        }

        return stream

    def stream_delete_range(self, start, end, keyword,
                            timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Deletes streams in a range of indexes [start, end] where the name includes keyword.

        :param start:
        :param end:
        :param keyword:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: None
        """

        for i in range(start, end + 1):
            stream = self.streams_get_by_id(i, timeout)
            json_stream = json.loads(stream.content)
            if 'name' in json_stream:

                if keyword.lower() in json_stream['name'].encode("ascii").lower():
                    self.stream_delete(i, timeout)
                    logging.info(f"Stream Deleted, {i}")
                else:
                    logging.info(f"Sensor not deleted {i}, no keyword match, stream name: {json_stream['name']}")

            else:
                logging.info(f"No name keyword in stream, stream doesn't exist. Stream Id: {i}")
        return
