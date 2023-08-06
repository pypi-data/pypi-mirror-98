"""
    Geostreams Sensors API.
"""
from __future__ import division

from builtins import object
import logging
import time
from datetime import datetime
from typing import Union, Tuple

from requests.exceptions import RequestException

from pygeostreams.client import GeostreamsClient


class SensorsApi(object):
    """
        API to manage the REST CRUD endpoints for sensors.
    """
    def __init__(self, client=None, host=None, username=None, password=None):
        """Set client if provided otherwise create new one"""
        if client:
            self.api_client = client
        else:
            self.client = GeostreamsClient(host=host, username=username, password=password)

    def sensors_get(self, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get the list of all available sensors.

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Getting all sensors")
        try:
            return self.client.get("/sensors", timeout)
        except RequestException as e:
            logging.error(f"Error retrieving sensor list: {e}")
            raise e

    def sensors_refresh_cache(self, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get all available sensors one by one, return nothing

        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :rtype: `requests.Response`
        """
        logging.debug("Getting all sensors by each id")
        try:
            sensor_list = self.client.get("/sensors", timeout)

            for sensor in sensor_list.json():
                logging.debug(f"refresh sensor {sensor['id']}")
                self.client.get("/sensors/%s" % sensor['id'])
                binning_filter = self.get_aggregation_bin(sensor['min_start_time'], sensor['max_end_time'])
                if sensor['properties']['type']['id'] == 'epa': 
                    binning_filter = 'semi'
                url = "/datapoints/bin/%s/1?sensor_id=%s" % (binning_filter, sensor['id'])
                self.client.get(url, timeout)
                time.sleep(100)     
            return True    
        except RequestException as e:
            logging.error(f"Error caching sensor list: {e}")
            raise e

    def sensor_refresh_cache(self, sensor_id,
                             timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get all available sensors one by one, return nothing

        :param sensor_id:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :rtype: `requests.Response`
        """
        logging.debug(f"prime cache for sensor {sensor_id}")
        try:
            response = self.client.get("/sensors/%s" % sensor_id, timeout)
            sensor = response.json()
            if 'min_start_time' not in sensor: 
                return False
            logging.debug("refresh sensor %s", sensor_id)
            self.client.get("/sensors/%s" % sensor_id, timeout)
            binningfilter = self.get_aggregation_bin(sensor['min_start_time'], sensor['max_end_time'])
            if sensor['properties']['type']['id'] == 'epa': 
                binningfilter = 'semi'

            self.client.get("/datapoints/bin/%s/1?sensor_id=%s" % (binningfilter, sensor_id), timeout)
    
            return True    
        except RequestException as e:
            logging.error(f"Error caching sensor: {e}")
            raise e

    def sensor_get(self, sensor_id, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get a specific sensor by id.

        :param sensor_id:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Sensor object as JSON.
        :rtype: `requests.Response`
        """
        logging.debug(f"Getting sensor {sensor_id}")
        try:
            return self.client.get("/sensors/%s" % sensor_id, timeout)
        except RequestException as e:
            logging.error(f"Error retrieving sensor {sensor_id}: {e}")
            raise e

    def sensor_get_by_name(self, sensor_name, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Get a specific sensor by id.

        :param sensor_name: Name of sensor
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Sensor object as JSON.
        :rtype: `requests.Response`
        """
        logging.debug(f"Getting sensor {sensor_name}")
        try:
            return self.client.get("/sensors?sensor_name=" + sensor_name, timeout)
        except RequestException as e:
            logging.error(f"Error retrieving sensor {sensor_name}: {e}")
            raise e

    def sensor_post(self, sensor, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Create sensor.

        :param sensor: Sensor json
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: sensor json.
        :rtype: `requests.Response`
        """
        logging.debug("Adding sensor")
        try:
            return self.client.post("/sensors", sensor, timeout)
        except RequestException as e:
            logging.error(f"Error adding sensor {sensor['name']}: {e}")
            raise e

    def sensor_post_json(self, sensor, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Create sensor.

        :param sensor: Sensor json
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: sensor json.
        :rtype: `requests.Response`
        """
        logging.debug("Adding or getting sensor")
        try:

            if 'id' in sensor:
                sensor_from_geostreams = self.sensor_get(sensor['id'], timeout).json()
            elif 'name' in sensor:
                sensor_from_geostreams = self.sensor_get_by_name(sensor['name'], timeout).json()

            if len(sensor_from_geostreams['sensors']) > 0:
                logging.info(f"Found sensor {sensor['name']}")
                return sensor_from_geostreams['sensors'][0]
            else:
                logging.info(f"Creating sensor with name: sensor['name']")
                sensor_id = (self.client.post("/sensors", sensor), timeout).json()
                sensor_from_geostreams = self.sensor_get(sensor_id['id'], timeout).json()
                return sensor_from_geostreams['sensor']
        except RequestException as e:
            logging.error(f"Error adding sensor {sensor['name']}: {e}")
            raise e

    def sensor_delete(self, sensor_id, timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Delete a specific sensor by id.

        :param sensor_id:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: If successful or not.
        :rtype: `requests.Response`
        """
        logging.debug(f"Deleting sensor {sensor_id}")
        try:
            return self.client.delete("/sensors/%s" % sensor_id, timeout)
        except RequestException as e:
            logging.error(f"Error retrieving sensor {sensor_id}: {e}")
            raise e

    def sensor_create_json(self, name, longitude, latitude, elevation, popup_content, region, huc=None, network=None,
                           organization_id=None, title=None):
        """Create sensor definition in JSON"""
        sensor = {
            "name": name,
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    longitude,
                    latitude,
                    elevation
                ]
            },
            "properties": {
                "name": name,
                "popupContent": popup_content,
                "region": region
            }
        }

        if network or id or title:
            sensor['properties']['type'] = {}

        if huc:
            sensor["properties"]["huc"] = huc
        if network:
            sensor['properties']['type']['network'] = network
        if organization_id:
            sensor['properties']['type']['id'] = organization_id
        if title:
            sensor['properties']['type']['title'] = title
        return sensor

    def sensor_statistics_post(self, sensor_id,
                               timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Update sensor statistics.
        :param sensor_id:
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Full list of sensors.
        :rtype: `requests.Response`
        """
        logging.debug("Updating sensor statistics")
        sensor = (self.sensor_get(sensor_id, timeout)).json()["sensor"]
        try:
            return self.client.put("/sensors/%s/update" % sensor_id, sensor, timeout)
        except RequestException as e:
            logging.error(f"Error updating sensor statistics for sensor {sensor_id}: {e}")
            raise e

    def get_aggregation_bin(self, start_time, end_time):
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
        year = end_time.year - start_time.year

        if year > 100: 
            time_bin = 'decade'
        elif year > 50: 
            time_bin = 'lustrum'
        elif year > 25:
            time_bin = 'year'
        elif year > 10:
            time_bin = 'season'
        elif year > 1:
            time_bin = 'month'
        else:
            diff_time = end_time - start_time
            b_time = divmod(diff_time.days * 86400 + diff_time.seconds, 60)[0]  # minutes
            b_time = b_time / 1440
            if b_time > 14:
                time_bin = 'day'
            elif b_time > 3:
                time_bin = 'hour'
            else:
                time_bin = 'minute'
        return time_bin

    def update_sensor_metadata(self, sensor,
                               timeout: Union[int, Tuple[int, int]] = (125, 605)):
        """
        Update sensor metadata
        :param sensor: Sensor json
        :param timeout: Number of seconds Requests will wait to establish a connection.
        Specify a Tuple if connect and read timeouts should be different (with the first element being
        the connection timeout, and the second being the read timeout.
        :return: Http response
        """
        logging.debug("Updating sensor's metadata")
        sensor_id = sensor["id"]
        try:
            return self.client.put("/sensors/%s" % sensor_id, sensor, timeout)
        except RequestException as e:
            logging.error(f"Error updating sensor metadata for sensor {sensor_id}: {e}")
            raise e
