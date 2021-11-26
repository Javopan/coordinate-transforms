from coordinate_transform import parse_text

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    coor_input = input('coordenadas a convertir: ')
    coordenadas = parse_text(coor_input, r'(\d{1,3}).(\d{1,2}).(\d{1,2}\.\d{1,3}).?([NSEWOnseow])?')
    if coordenadas.lastindex >= 3:
        c1 = float(coordenadas[1])
        c2 = float(coordenadas[2])
        c3 = float(coordenadas[3])
        c4 = coordenadas[4].lower()
        # adds a negative symbols if it is west or south
        c_decimal = c1 + c2/60 + c3/3600
        if c4 == 's' or c4 == 'w' or c4 =='o':
            c_decimal *= -1
        print(c_decimal)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
