# This is a sample Python script.
import re
import subprocess
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def parse_text(text, regular_exp):
    """
    This function will parse the text using a regular expression and return the result
    :param regular_exp: str, regular exprenssion
    :return: list, will have the matched regular expression if any
    """
    match = re.compile(regular_exp)
    result = match.search(text)
    return result

def transform():
    coor_input = input('coordenadas a convertir: ')
    coordenadas = parse_text(coor_input, r'(\d{1,3}).(\d{1,2}).(\d{1,2}\.\d{1,3}).?([NSEWOnseow])?')
    if coordenadas.lastindex >= 3:
        c1 = float(coordenadas[1])
        c2 = float(coordenadas[2])
        c3 = float(coordenadas[3])
        c4 = coordenadas[4].lower()
        # adds a negative symbols if it is west or south
        c_decimal = c1 + c2 / 60 + c3 / 3600
        if c4 == 's' or c4 == 'w' or c4 == 'o':
            c_decimal *= -1
        print(c_decimal)