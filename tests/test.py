#coding: UTF-8
#Geographic midpoint
#http://www.geomidpoint.com/meet/
#http://www.geomidpoint.com/calculation.html
from math import (pi, sin, cos, atan2, sqrt)
from get_mid_point import (pygmapslib, directions, geocoding)
from StringIO import StringIO
import sys


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

point1 = geocoding.request('Tokyo')
point2 = geocoding.request('Osaka')
point3 = geocoding.request('Nagoya')
middle_cord = get_middle_point([point1.data[0]['geometry']['location'], point2.data[0]['geometry']['location'], point3.data[0]['geometry']['location']])
middle_point = geocoding.request(str(middle_cord['lat']) + ',' + str(middle_cord['lng']))

results = directions.request(origin='Tokyo', destination=str(middle_point.data[0]['geometry']['location']['lat']) + ',' + str(middle_point.data[0]['geometry']['location']['lng']))

output = StringIO()
for route in results.data:
    output.write(u'ルートサマリ: ' + route['summary'])
    for leg in route['legs']:
        output.write(u'出発地点: ' + leg['start_address'])
        output.write(u'到着地点: ' + leg['end_address'])
        output.write(u'距離: ' + leg['distance']['text'])
        output.write(u'所要時間: ' + leg['duration']['text'])
        for step in leg['steps']:
            output.write(step['html_instructions'])
print output.getvalue().encode(sys.getfilesystemencoding())


