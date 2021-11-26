from coordinate_transform import parse_text, transform
from kml_parser import kml_process

# Press the green button in the gutter to run the script.
eventos = {
        'transform': transform,
        '1': transform,
        'kmz': kml_process,
        '2': kml_process,
    }

if __name__ == '__main__':
    print('Welcome to Javopan handy tools.')
    print('please select one of the following functions or number:\n')
    print('\t1- transform: changes coordinates from DMS to Decimal degree')
    print('\t2- kmz: parses a kmz/kml file to extract placemakrs and coordines of it')
    print('\t0- x: quits the program')
    print()
    event = -1
    while event != 'x':
        event = input('What program do you want to use:')
        try:
            eventos[event]()
        except:
            print('Please a select valid option')
    print('Thanks for using my tools')




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
