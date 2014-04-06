#coding: UTF-8
import sys
import traceback
from pygmapslib import PyGMaps, PyGMapsError

__all__ = ['GeocodingError', 'Geocoding', 'request']

class GeocodingError(Exception):
    def __init__(self, error_status, params):
        self.error_status = error_status
        self.params = params

    def __str__(self):
        return self.error_status + '\n' + str(self.params)

    def __unicode__(self):
        return unicode(self.__str__())

class Geocoding(object):
    def __init__(self, data):
        self.data = data

    def __unicode__(self):
        addresses = ''
        for result in self.data:
            addresses = addresses + result['formatted_address'] + '\n'
        return addresses

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()

    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')

def request(address, sensor='false', gmaps = None):

    query_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'address': address,
        'sensor' : sensor
    }

    try:
        if gmaps is None:
            gmap_result = PyGMaps().get_data(query_url, params)
        else:
            gmap_result = gmaps.get_data(query_url, params)

    except PyGMapsError as e:
        print traceback.format_exc()
        raise GeocodingError('HTTP STATUS ERROR', params)

    if gmap_result['status'] != 'OK':
        raise GeocodingError(gmap_result['status'], params)

    return Geocoding(gmap_result['results'])

