"""
    Geostreams Datapoints API
"""

from builtins import str
from builtins import object
import logging

from typing import Union, Tuple
from dateutil.parser import parse
from requests.exceptions import RequestException

from pygeostreams.client import GeostreamsClient


class DatapointsApi(object):
    """
        API to manage the REST CRUD endpoints for datapoints.
    """
    def __init__(self, client=None, host=None, username=None, password=None):
        """Set client if provided otherwise create new one"""
        if client:
            self.api_client = client
        else:
            self.client = GeostreamsClient(host=host, username=username, password=password)

    def datapoint_post(self, datapoint, timeout: Union[int, Tuple[int, int]] = (120, 600)):
        """
        Add a datapoint.

        :param datapoint:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: If successful or not.
        :rtype: `requests.Response`
        """
        logging.debug("Adding datapoint")
        try:
            return self.client.post("/datapoints", datapoint, timeout)
        except RequestException as e:
            logging.error(f"Error adding datapoint {datapoint}: {e}")
            raise e

    def datapoints_count_by_sensor_get(self, sensor_id,
                                       timeout: Union[int, Tuple[int, int]] = (120, 600)):
        """
        Get the list of all available sensors.

        :param sensor_id:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Counting datapoints by sensor")
        try:
            return self.client.get("/datapoints?sensor_id=%s&onlyCount=true" % sensor_id, timeout)
        except RequestException as e:
            logging.error(f"Error counting datapoints by sensor {sensor_id}: {e}")
            raise e

    def datapoint_latest_get(self, sensor_id, stream_id, since=None,
                             timeout: Union[int, Tuple[int, int]] = (120, 600)):
        """
        Get latest datapoint for a given stream by retrieving datapoint since a recent date and then grabbing
        the latest one.

        TODO: this should be an API endpoint
        """
        latest_datapoint = None
        # logging.info("Getting datapoints for stream %s since %s " % stream_id, since)
        if since is None:
            url = "/datapoints?stream_id=%s" % stream_id
        else:
            url = "/datapoints?stream_id=%s&since=%s" % (stream_id, since)
        try:
            datapoints = self.client.get_json(url, timeout)
            if isinstance(datapoints, list) and len(datapoints) > 0:
                latest_datapoint = datapoints[-1]
                start_date = parse(latest_datapoint['start_time']).strftime('%Y-%m-%d-%H-%M')
                logging.info(f"Fetched datapoints for {sensor_id} starting on {start_date}")
            else:
                logging.debug(f"No datapoints exist for {sensor_id}")
        except RequestException as e:
            logging.error(f"Error getting datapoints for stream {stream_id} since {since}: {e}")
            raise e

        return latest_datapoint

    def datapoint_create_json(self, start_time, end_time, longitude, latitude, sensor_id, stream_id, sensor_name,
                              properties=None, owner=None, source=None, procedures=None, elevation=0):
        """
        Create a json representation of a datapoint

        :param start_time:
        :param end_time:
        :param longitude:
        :param latitude:
        :param sensor_id:
        :param stream_id:
        :param sensor_name:
        :param properties:
        :param owner:
        :param source:
        :param procedures:
        :param elevation:
        :return:
        """
        datapoint = {
            'start_time': start_time,
            'end_time': end_time,
            'type': 'Feature',
            'geometry': {
                'type': "Point",
                'coordinates': [
                    longitude,
                    latitude,
                    elevation
                ]
            },
            'stream_id': str(stream_id),
            'sensor_id': str(sensor_id),
            'sensor_name': str(sensor_name)
        }

        if properties is not None:
            datapoint['properties'] = properties
            datapoint['properties']['site'] = sensor_name
            if owner is not None:
                datapoint['properties']["owner"] = owner
            if source is not None:
                datapoint['properties']['source'] = source
            if procedures is not None:
                datapoint['properties']['procedures'] = procedures

        return datapoint

    def datapoint_create_bulk(self, datapoints, timeout: Union[int, Tuple[int, int]] = (120, 600)):
        """

        :param datapoints:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return:
        """
        logging.debug("Adding Datapoints in Bulk")
        try:
            return self.client.post("/datapoints/bulk", datapoints, timeout)
        except RequestException as e:
            logging.error(f"Error adding bulk datapoint: {e}")
            raise e


    def get_datapoints_by_sensor_id(self, sensor_id, since=None, until=None):

        if since is None and until is None:
            url = '/datapoints?sensor_id=%s' % sensor_id
        elif since is None and until is not None:
            url = "/datapoints?sensor_id=%s&until=%s" % (sensor_id, until)
        elif since is not None and until is None:
            url = "/datapoints?sensor_id=%s&since=%s" % (sensor_id, since)
        elif since is not None and until is not None:
            url = "/datapoints?sensor_id=%s&since=%s&until=%s" % (sensor_id, since, until)

        try:
            return self.client.get(url)
        except Exception as e:
            logging.error("Error getting datapoints from sensor %s: " % sensor_id, e.message)
            raise e
