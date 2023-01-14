import math


class Earthquake:
    """A class to represent an Earthquake."""
    def __init__(self, place, mag, longitude, latitude, time):
        self.place = place
        self.mag = mag
        self.longitude = longitude
        self.latitude = latitude
        self.time = time

    def __eq__(self, other):
        return (
            (self.place == other.place) and
            math.isclose(self.mag, other.mag) and
            math.isclose(self.longitude, other.longitude) and
            math.isclose(self.latitude, other.latitude) and
            (self.time == other.time)
        )


# NOTE: This function takes an already open file as input.  You *will not*
# be opening anything in this function.
def read_quakes_from_file(file):
    split_list = []
    list_line = []
    for line in file:
        line_strip = line.strip()
        split_list.append(line_strip.split(' ', 4))
    for each_line in split_list:
        list_line.append(asign_earthquakes(each_line))
    return list_line


def asign_earthquakes(list):
    place = str(list[4])
    mag = float(list[0])
    longitude = float(list[1])
    latitude = float(list[2])
    time = int(list[3])
    return (Earthquake(place, mag, longitude, latitude, time))


def filter_by_mag(quakes, low, high):
    list_by_mag = []
    for line in quakes:
        mag = line.mag
        if float(low) <= mag <= float(high):
            list_by_mag.append(line)
    return list_by_mag


def filter_by_place(quakes, word):
    list_by_place = []
    new_word = word.upper()
    for line in quakes:
        place = line.place
        new_place = place.upper()
        if new_word in new_place:
            list_by_place.append(line)
    return list_by_place


def sort_mag(one_quakes):
    return one_quakes.mag


def sort_by_mag(quakes):
    quakes.sort(key=sort_mag, reverse=True)
    return quakes


def sort_time(one_quakes):
    return one_quakes.time


def sort_by_time(quakes):
    quakes.sort(key=sort_time, reverse=True)
    return quakes


def sort_longitude(one_quakes):
    return one_quakes.longitude


def sort_by_longitude(quakes):
    quakes.sort(key=sort_longitude)
    return quakes


def sort_latitude(one_quakes):
    return one_quakes.latitude


def sort_by_latitude(quakes):
    quakes.sort(key=sort_latitude)
    return quakes


def raw_feature(list):
    new_list = []
    for quake in list:
        place = str(quake.place)
        mag = str(quake.mag)
        longitude = str(quake.longitude)
        latitude = str(quake.latitude)
        time = str(quake.time)
        line = mag + ' ' + longitude + ' ' + \
            latitude + ' ' + time + ' ' + place + '\n'
        new_list.append(line)
    return new_list


def quake_from_feature(feature):
    mag = float(feature['properties']['mag'])
    time = int(feature['properties']['time'] / 1000)
    longitude = float(feature['geometry']['coordinates'][0])
    latitude = float(feature['geometry']['coordinates'][1])
    place = str(feature['properties']['place'])
    return Earthquake(place, mag, longitude, latitude, time)
