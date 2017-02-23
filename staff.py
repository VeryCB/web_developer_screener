import json
from math import sin, cos, asin, sqrt, radians

from flask import Flask
from flask import render_template

app = Flask(__name__)

STAFF_DATA_FILE = 'staff_list.json'

EARTH_RADIUS = 6371000  # metres

OFFICE_LATITUDE = -41.2920728
OFFICE_LONGITUDE = 174.7748162
DISTANCE_THRESHOLD = 2000  # metres


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points using haversine formula

    :param lat1: the fist point's latitude
    :param lon1: the fist point's longitude
    :param lat2: the second point's latitude
    :param lon2: the second point's longitude
    """

    # convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    d_lat = abs(lat2 - lat1)
    d_lon = abs(lon2 - lon1)

    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    central_angle = 2 * asin(sqrt(a))

    return EARTH_RADIUS * central_angle


def test_calculate_distance():
    assert calculate_distance(OFFICE_LATITUDE, OFFICE_LONGITUDE,
        -41.268897832897466, 174.7525605490229) == 3177.920085373409


@app.route("/")
def staff_list():
    with open(STAFF_DATA_FILE) as data_file:
        data = json.load(data_file)

    filterd_staff = []

    for staff in data['staff']:
        location = staff['location']
        distance = calculate_distance(OFFICE_LATITUDE, OFFICE_LONGITUDE,
                                      location['latitute'],
                                      location['longitude'])

        if distance < DISTANCE_THRESHOLD:
            filterd_staff.append(staff)

    sorted_staff = sorted(filterd_staff, key=lambda s: s['name'])
    return render_template('staff_list.html', staff_list=sorted_staff)


if __name__ == "__main__":
    app.run()
