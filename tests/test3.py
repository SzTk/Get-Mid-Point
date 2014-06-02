#coding: UTF-8
#Geographic midpoint
#http://www.geomidpoint.com/meet/
#http://www.geomidpoint.com/calculation.html
from math import (pi, sin, cos, atan2, sqrt)
from get_mid_point import (pygmapslib, directions, geocoding, placesearch, shortest_path)
LINE_FILE = './train_data/line20140303free.csv'
STATION_FILE = './train_data/station20140303free.csv'
JOIN_FILE = './train_data/join20140303.csv'

def get_average(length1, length2, length3):
    return (length1+length2+length3)/3

def get_middle_point(coordinates):
    x = 0
    y = 0
    z = 0
    for point in coordinates:
        x = x + cos(point['lat'] * pi / 180) * cos(point['lng'] * pi /180)
        y = y + cos(point['lat'] * pi / 180) * sin(point['lng'] * pi /180)
        z = z + sin(point['lat'] * pi / 180)
    x = x / len(coordinates)
    y = y / len(coordinates)
    z = z / len(coordinates)
    return {'lng' : atan2(y,x) * 180 / pi, 'lat' : atan2(z, sqrt(x*x + y*y)) * 180 /pi}

def get_shortest_path_index(sp, stations, point1, point2, point3):
    time_diff = []
    for result in stations.data:
        max_time_diff = 0
        length1 = sp.shortest_path_length_with_locations(result['geometry']['location'],point1.data[0]['geometry']['location'])
        length2 = sp.shortest_path_length_with_locations(result['geometry']['location'],point2.data[0]['geometry']['location'])
        length3 = sp.shortest_path_length_with_locations(result['geometry']['location'],point3.data[0]['geometry']['location'])
        average_length = get_average(length1, length2, length3)
        if( max_time_diff < abs(length1 - average_length) ):
            max_time_diff = abs(length1 - average_length)
        if( max_time_diff < abs(length2 - average_length) ):
            max_time_diff = abs(length2 - average_length)
        if( max_time_diff < abs(length3 - average_length) ):
            max_time_diff = abs(length3 - average_length)
        time_diff.append(max_time_diff)
    return time_diff.index(min(time_diff))

def test_mid_point():
    sp = shortest_path.ShortestPath(STATION_FILE,
                                    LINE_FILE,
                                    JOIN_FILE)
    point1 = geocoding.request('中野島駅')
    point2 = geocoding.request('武蔵小山駅')
    point3 = geocoding.request('鴨宮駅')
    middle_cord = get_middle_point([point1.data[0]['geometry']['location'], point2.data[0]['geometry']['location'], point3.data[0]['geometry']['location']])
    stations = placesearch.get_nearest_station(middle_cord, key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    shortest_path_index = get_shortest_path_index(sp, stations, point1, point2, point3)
    print stations.data[shortest_path_index]['name']

if __name__ == '__main__':
    LINE_FILE = '../train_data/line20140303free.csv'
    STATION_FILE = '../train_data/station20140303free.csv'
    JOIN_FILE = '../train_data/join20140303.csv'
    test_mid_point()