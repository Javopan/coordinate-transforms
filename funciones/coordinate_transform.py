from funciones.texto import parse_text
# Press Shift+F10 to execute it or replace it with your code.


def transform(txt_input):
    """
    Stplit the input into 2 fields latitude and longitude
    :param txt_input: text to split
    :return: float, returns the transformed coordinate
    """
    # coor_input = input('coordenadas a convertir: ')
    coordenadas = parse_text(txt_input, r'[^0-9]*?(\d{1,3}).+?(\d{1,2}).+?(\d{1,2}(\.\d{1,5})?).*?([NSEWOnseow])')
    if coordenadas is not None and coordenadas.lastindex >= 3:
        c1 = float(coordenadas[1])
        c2 = float(coordenadas[2])
        c3 = float(coordenadas[3])
        c4 = coordenadas[5].lower()
        # adds a negative symbols if it is west or south
        c_decimal = c1 + c2 / 60 + c3 / 3600
        if c4 == 's' or c4 == 'w' or c4 == 'o':
            c_decimal *= -1
        if c4 == 'n' or c4 == 's':
            if -90 <= c_decimal <= 90:
                return round(c_decimal, 8)
            else:
                return 'Latitude can only be between -90 to 90 degrees. Check the point!'
        elif c4 == 'e' or c4 == 'w' or c4 == 'o':
            if -180 <= c_decimal <= 180:
                return round(c_decimal, 8)
            else:
                return 'Longitude can only be between -180 to 180 degrees. Check the point!'
        else:
            return 'you are missing the direction please add N, S, E or W!'
    return 'Please check the format is DD°MM\'SS.SS[N,E,S,W]!'
