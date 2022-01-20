import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox
from funciones.matrix_link_calculator import calculate_azimuth
import requests
import json


def get_profile(lat1, lon1, lat2, lon2, key, samples=100):
    url = "https://maps.googleapis.com/maps/api/elevation/json?" \
          f"path={lat1}%2C{lon1}%7C{lat2}%2C{lon2}&samples={samples}&key={key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return -1


def check_los(los_profile, start_hei, target_hei, start_name, target_name, distance, image=True):
    """
    Checks if there is LoS between 2 points with certain height
    :param target_name: str, name of the target
    :param start_name: str, name of the start
    :param los_profile: dict, results as is from google elevation API
    :param start_hei:  float, start height
    :param target_hei: float, end height
    :return: plt plot if there is LoS else returns -1
    """
    # ecuation: y = mx + b

    los_profile = los_profile['results']
    elevation_list = []
    for tick in los_profile:
        elevation_list.append(tick['elevation'])

    resolution = len(elevation_list)
    elevation_list = np.array(elevation_list)

    start_hei = start_hei + elevation_list[0]
    target_hei = target_hei + elevation_list[-1]

    b = start_hei
    height_dif = start_hei - target_hei
    m = -height_dif / resolution

    x = np.array(range(resolution))
    y = x * m + b
    # values to divide the distance in resolution steps
    x_labels = np.array(range(1, resolution+1)) * (distance / resolution)
    # we check if there is LoS
    los = all(y > elevation_list)
    if image and los:
        # create subplot
        f, ax = plt.subplots(figsize=(10.5, 8))
        # do the graphs with the modified range
        ax.plot(x_labels, elevation_list, color='brown')
        ax.plot(x_labels, y, color='green')
        # set title to the plot
        ax.set_title(f'Link {start_name} to {target_name}')
        # create vertical lines with tower height
        ax.vlines(x_labels[0], elevation_list[0], start_hei)
        ax.vlines(x_labels[-1], elevation_list[-1], target_hei)
        # set axes labels
        ax.set_ylabel('Height in m')
        ax.set_xlabel(f'{distance} km')
        # graph title
        ax.legend(['Terrain profile', 'Wireless link'])
        max_elev = max(elevation_list)
        # ading info to the start tower
        tower_start = start_hei - elevation_list[0]
        y_start = tower_start / 2 + elevation_list[0]
        x_start = x_labels[2]
        ax.text(x_start, y_start, f'{round(tower_start,2)}m')
        # ading info to the end tower
        tower_end = target_hei - elevation_list[-1]
        y_target = tower_end / 2 + elevation_list[-1]
        x_target = x_labels[-8]
        ax.text(x_target, y_target, f'{round(tower_end,2)}m')
        # add table with data
        labels_cols = ['Start', 'Distance', 'End']
        labels_rows = ['Name', 'Lat', 'Lon', 'Tower height', 'Terrain height', 'Az.']
        az_t2e = calculate_azimuth(los_profile[0]["location"]["lat"], los_profile[0]["location"]["lng"],
                                   los_profile[-1]["location"]["lat"], los_profile[-1]["location"]["lng"])
        az_e2t = calculate_azimuth(los_profile[-1]["location"]["lat"], los_profile[-1]["location"]["lng"],
                                   los_profile[0]["location"]["lat"], los_profile[0]["location"]["lng"])
        data = [
            [f'{start_name}', f'{distance} km', f'{target_name}'],
            [f'{los_profile[0]["location"]["lat"]}°', '', f'{los_profile[-1]["location"]["lng"]}°'],
            [f'{los_profile[0]["location"]["lat"]}°', '', f'{los_profile[-1]["location"]["lng"]}°'],
            [f'{round(tower_start,2)} m', '', f'{round(tower_end,2)} m'],
            [f'{elevation_list[0]}', '', f'{elevation_list[-1]}'],
            [f'{az_t2e}°', '', f'{az_e2t}°']
        ]
        plt.table(cellText=data, rowLabels=labels_rows, colLabels=labels_cols, loc='bottom', cellLoc='center',
                  bbox=(0, -0.35, 1, 0.25))
        f.tight_layout()

    return los, (f, ax) if image and los else None


def save_graph(filename, list_graph, single=True):
    if single:
        fig = list_graph[0][0]
        fig.savefig(filename)
    else:
        with PdfPages(filename) as pdf:
            for graph in list_graph:
                pdf.savefig(graph[0])


if __name__ == '__main__':
    key_input = input('what\'s your key: ')
    print(get_profile('36.578581', '-118.291994', '36.23998', '-116.83171', key_input, 100))
