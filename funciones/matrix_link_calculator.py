import numpy as np
import pandas as pd
from haversine import haversine_vector
from collections import OrderedDict


def calculate_matrix(pops, sites, distance_threshold):
    """
    Calculates a distance matrix between points and will break at distance_threshold
    :param pops: str, path to file with the pops
    :param sites: str, path to file with the sites
    :param distance_threshold: int, distance threshold on the calculated links
    :return: dataframe, a dataframe with the sites on the rows and the pops on the columns
    """

    # Checks if the in file is XLSX or CSV
    if 'xlsx' in pops:
        df_pops = pd.read_excel(pops)
    else:
        df_pops = pd.read_csv(pops)

    if 'xlsx' in sites:
        df_sites = pd.read_excel(sites)
    else:
        df_sites = pd.read_csv(sites)

    max_distance = distance_threshold

    # lists that will hold all the coordinates of each site to be able to process it with numpy
    pops_list = []
    site_list = []

    # dictionary with all the links
    all_dict = OrderedDict()

    for row in df_pops.iterrows():
        name = row[1]['Node Name']
        lati = row[1]['Latitude']
        long = row[1]['Longitude']
        h = row[1]['Height']
        pops_list.append((lati, long))
        if name not in all_dict:
            all_dict[name] = {'lat': lati, 'lon': long, 'hei': h}

    for row in df_sites.iterrows():
        name = row[1]['Node Name']
        lati = row[1]['Latitude']
        long = row[1]['Longitude']
        h = row[1]['Height']
        site_list.append((lati, long))
        if name not in all_dict:
            all_dict[name] = {'lat': lati, 'lon': long, 'hei': h}

    # Calculamos el haversine en matriz. las columnas son los POPS los renglones son los
    # sites
    df_link_matrix = pd.DataFrame(haversine_vector(pops_list, site_list, comb=True))
    df_link_matrix.columns = list(df_pops['Node Name'])
    df_link_matrix.index = list(df_sites['Node Name'])

    dict_sites = OrderedDict()

    for row in df_link_matrix.iterrows():
        links_in_distance = row[1][row[1] < max_distance]
        if len(links_in_distance) > 0:
            dict_conections = OrderedDict()
            update = False
            for name, distance in links_in_distance.items():
                if distance > 0.01:
                    update = True
                    lat1 = all_dict[row[0]]['lat']
                    lon1 = all_dict[row[0]]['lon']
                    lat2 = all_dict[name]['lat']
                    lon2 = all_dict[name]['lon']
                    dict_conections[name] = (lat2, lon2, all_dict[name]['hei'], distance,
                                             calculate_azimuth(lat1, lon1, lat2, lon2),
                                             calculate_azimuth(lat2, lon2, lat1, lon1))
            if len(dict_conections) > 0 and update:
                dict_sites[row[0]] = {'lat': lat1, 'lon': lon1, 'hei': all_dict[row[0]]['hei']}
                dict_sites[row[0]].update(dict_conections)

    return dict_sites, all_dict, len(pops_list), len(site_list)


def calculate_azimuth(lat1, lon1, lat2, lon2):
    """
    Calculates the azimuth from 2 coordinates
    :param lat1: float, latitude in degrees point 1
    :param lon1: float, longitude in degrees point 1
    :param lat2: float, latitude in degrees point 2
    :param lon2: float, longitude in degrees point 2
    :return: azimuth in degrees
    """
    lat1_r = np.deg2rad(lat1)
    lon1_r = np.deg2rad(lon1)
    lat2_r = np.deg2rad(lat2)
    lon2_r = np.deg2rad(lon2)

    delta_lons = lon2_r - lon1_r

    azimuth = np.arctan2((np.sin(delta_lons) * np.cos(lat2_r)),
                         (np.cos(lat1_r) * np.sin(lat2_r) - np.sin(lat1_r) * np.cos(lat2_r) * np.cos(delta_lons)))
    azimuth = np.round(np.rad2deg(azimuth), 2)
    return azimuth if azimuth > 0 else azimuth + 360


def write_to_excel(dict_link, filename):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(f'site_name,site_lat,site_lon,site_height,distance_to_pop in km,pop_name,pop_lat,pop_lon,pop_height,'
                   f'Pop->Site  Azimuth,Site->POP  Azimuth\n')
        for start, links in dict_link.items():
            for end, data in links.items():
                if (end == 'lat' and isinstance(data, float)) or (end == 'lon' and isinstance(data, float)) \
                        or (end == 'hei' and isinstance(data, float)):
                    continue
                file.write(f'{start},{dict_link[start]["lat"]},{dict_link[start]["lon"]},{dict_link[start]["hei"]},'
                           f'{round(data[3],2)},{end},'
                           f'{data[0]},{data[1]},{data[2]},'
                           f'{round(data[4],2)},{round(data[5],2)}\n')
