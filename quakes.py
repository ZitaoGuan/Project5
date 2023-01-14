from utils import time_to_str, get_json
import quake_funcs
import sys


def main():
    file = open(sys.argv[1], 'r')
    list_line = quake_funcs.read_quakes_from_file(file)
    output(list_line)
    file.close()
    new_list = list_line
    fil = option()
    while fil != 'q' and fil != 'Q':
        if fil == 's' or fil == 'S':
            new_list = option_sort(list_line)
            fil = option()
        elif fil == 'f' or fil == 'F':
            print_filter(list_line)
            fil = option()
        elif fil == 'n' or fil == 'n':
            new_list = option_new(list_line)
            number = not_in_list(new_list)
            option_read_new(new_list, number)
            fil = option()
    add_file(new_list, sys.argv[1])
    quit()


def add_file(list_quakes, file_old):
    file = open(file_old, 'w')
    file_quakes = quake_funcs.raw_feature(list_quakes)
    for quakes in file_quakes:
        file.write(quakes)
    print()
    file.close()


def option():
    print("\nOptions:")
    print(
        '  (s)ort\n  (f)ilter\n  (n)ew quakes\n  (q)uit\n'
    )
    return input('Choice: ')


def option_sort(file):
    input_sort = input(
        'Sort by (m)agnitude, (t)ime, (l)ongitude, or l(a)titude? '
    )
    print("\nEarthquakes:")
    print("------------")
    if input_sort == 'm' or input_sort == 'M':
        new_list = sort_m(file)
    elif input_sort == 'T' or input_sort == 't':
        new_list = sort_t(file)
    elif input_sort == 'l' or input_sort == 'L':
        new_list = sort_l(file)
    elif input_sort == 'a' or input_sort == 'A':
        new_list = sort_a(file)
    read_text(new_list)
    return new_list


def read_text(list):
    for line in list:
        mag = line.mag
        place = line.place
        time = time_to_str(line.time)
        longitude = line.longitude
        latitude = line.latitude
        print(
            "(%.2f) %40s at %s (%8.3f, %8.3f)" % (
                mag, place, time, longitude, latitude
            )
        )


def sort_m(file):
    new_list = quake_funcs.sort_by_mag(file)
    return new_list


def sort_t(file):
    new_list = quake_funcs.sort_by_time(file)
    return new_list


def sort_l(file):
    new_list = quake_funcs.sort_by_longitude(file)
    return new_list


def sort_a(file):
    new_list = quake_funcs.sort_by_latitude(file)
    return new_list


def output(files):
    print("Earthquakes:")
    print("------------")
    for line in files:
        mag = line.mag
        place = line.place
        time = time_to_str(line.time)
        longitude = line.longitude
        latitude = line.latitude
        print(
            "(%.2f) %40s at %s (%8.3f, %8.3f)" % (
                mag, place, time, longitude, latitude
            )
        )


def print_filter(file):
    input_sort = input(
        'Filter by (m)agnitude or (p)lace? '
    )
    if input_sort == 'p' or input_sort == 'P':
        list_place = filter_place(file)
        print("\nEarthquakes:")
        print("------------")
        read_text(list_place)
    elif input_sort == 'M' or input_sort == 'm':
        list_mag = filter_mag(file)
        print("\nEarthquakes:")
        print("------------")
        read_text(list_mag)


def filter_place(file):
    string = input(
        'Search for what string? '
    )
    list_string = quake_funcs.filter_by_place(file, string)
    return list_string


def get_feature(url):
    quakes_dictionary = get_json(url)
    new_list = []
    for feature in quakes_dictionary['features']:
        new_list.append(
            quake_funcs.quake_from_feature(feature)
        )
    return new_list


def filter_mag(file):
    low = input('Lower bound: ')
    up = input('Upper bound: ')
    list_mag = quake_funcs.filter_by_mag(file, low, up)
    return list_mag


def option_new(current_list):
    url = 'http://earthquake.usgs.gov/'\
        'earthquakes/feed/v1.0/summary/1.0_hour.geojson'
    list_quakes = get_feature(url)
    for quakes in list_quakes:
        if quakes not in current_list:
            current_list.append(quakes)
    return (current_list)


def option_read_new(current_list, number):
    if number == 0:
        print('\nNew quakes found!!!')
    print('\nEarthquakes:')
    print('------------')
    read_text(current_list)


def not_in_list(current_list):
    url = 'http://earthquake.usgs.gov/'\
        'earthquakes/feed/v1.0/summary/1.0_hour.geojson'
    num = 0
    list_quakes = get_feature(url)
    for quakes in list_quakes:
        if quakes in current_list:
            num += 1
    return num

main()
