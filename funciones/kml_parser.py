from zipfile import ZipFile
from bs4 import BeautifulSoup
from haversine import haversine_vector, Unit

import pandas as pd


def kml_parse():
    """
    Parses a KMZ or KML file to get all the placemarks in a file and returns a matrix on the format
    [
    [Name, lat, lon, height]
    [Name, lat, lon, height]
    ]
    :return: list
    """

    def process_kmz(file):
        """
        Changes a file from KMZ to KML
        :param file: path of the file to change
        :return: kml file
        """
        try:
            file_kmz = ZipFile(file, 'r')
            with file_kmz.open('doc.kml', 'r') as f:
                return f.read()
        except:
            print('Something went wrong. Could not read the file. Make sure the path and the file exists\n'
                  'the file given is:\n'
                  f'{file}')
            return -1

    file = input(r'please input the file name with the path: (e.g. c:\Downloads\file.kmz)')

    if file[file.rfind('.') + 1:] == 'kmz':  # convert KMZ to KML
        file_kml = process_kmz(file)
    elif file[file.rfind('.') + 1:] == 'kml':  # open KML file
        with open(file, 'r') as f:
            file_kml = f.read()
    else:
        print('Invalid file type, please select a valid kmz or kml file')
        return []

    # we create a soup parsing via lxml
    file_bs = BeautifulSoup(file_kml, 'lxml')

    # holder for the places, each place is a list inside the list
    places = []
    # we iterate over all placemarks
    for placemark in file_bs.find_all('placemark'):
        name_txt = placemark.find('name').text  # name of the placemark
        # only placemarks with lat, lon and height are points, everything else is another type of placemark
        if len(placemark.find('coordinates').text.split(',')) == 3:
            place_name = placemark.find('name').text
            place_lon, place_lat, place_hei = placemark.find('coordinates').text.split(',')
            places.append([place_name, place_lat, place_lon, place_hei])
    return places


def kml_process():
    """
    This process will create a pandas dataframe with the information of the lat lon and height.
    Will save a file with the haversine distance between points
    :return:
    """
    kml_points = kml_parse()
    points_a = pd.DataFrame(kml_points)
    points_b = pd.DataFrame(kml_points)

    points_a_clean = points_a.drop([0, 3], axis=1).astype('float')
    points_b_clean = points_b.drop([0, 3], axis=1).astype('float')

    link_matrix = pd.DataFrame(haversine_vector(points_a_clean, points_b_clean, Unit.KILOMETERS, comb=True),
                               columns=list(points_a[0]),
                               index=list(points_a[0]))

    link_matrix.to_csv('link_matrix.csv')
