import copy
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QTreeWidgetItem
from gui.MatrixCalculator import Ui_MatrixCalculator
from funciones.pyqt_functions import open_dialog, log_message
from funciones.matrix_link_calculator import calculate_matrix, write_to_excel
from funciones.google_profile import get_profile, check_los, save_graph, find_best_height
import os
import pickle


class MatrixCalculator(QWidget, Ui_MatrixCalculator):
    def __init__(self, parent):
        super(MatrixCalculator, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.all_sites = None  # Diccionario con la información de todos los sitios. Solo se genera con archivos
        self.pops = None  # Número total de pops
        self.targets = None  # número total de sites
        self.dict_links = None  # diccionario con toda la información de los sitios y los enlaces de cada sitio
        self.single_profile = None  # info para guardar un solo perfil si se hace un check
        self.all_profiles = None  # todos los perfiles cuando se corre el check de revisar todos
        self.table_expanded = False  # variable para poder llevar control de si los elementos están extendidos o no
        self.graph_book = None

        # Treewidget setup
        self.tbl_linksmatrix.setColumnCount(8)
        # Labels for the trees
        self.tbl_linksmatrix.setHeaderLabels(['Sites', 'Target', 'Lat', 'Lon', 'Distance', 'Height', 'Max. Height',
                                              'Azimuth', 'Rev. Azimuth'])

        # click actions
        self.bnt_load_pops.clicked.connect(self.load_pops)
        self.bnt_load_nodes.clicked.connect(self.load_nodes)
        self.bnt_calculate_links.clicked.connect(self.calculate_matrix)
        self.bnt_getprofiles.clicked.connect(self.get_profile_all)
        self.bnt_getprofile.clicked.connect(self.get_profile)
        self.bnt_loadprofiles.clicked.connect(self.load_los)
        self.bnt_calculatelos_all.clicked.connect(self.calculate_los_all)
        self.bnt_calculatelos_single.clicked.connect(self.calculate_los)
        self.bnt_generatekml.clicked.connect(self.generate_kml)
        self.bnt_save_excel.clicked.connect(self.save_excel)
        self.tbl_linksmatrix.doubleClicked.connect(self.expand_table)
        self.btn_optimize_heights.clicked.connect(self.optimize_heights)

        # names of the files to open
        self.pops_f = None
        self.sites_f = None

    def generate_kml(self):
        print('Generar un KML')

    def optimize_heights(self, single=True):
        if single:
            if self.single_profile:
                tree_line = self.tbl_linksmatrix.selectedItems()
                parent = tree_line[0].parent() if tree_line else None
                if parent:
                    target_name = tree_line[0].text(1)
                    target_hei = tree_line[0].text(4)
                    parent_name = parent.text(0)
                    parent_hei = parent.text(4)
                    link_distance = tree_line[0].text(5)
                    link_distance = float(link_distance[:link_distance.rfind(' km')])

                    find_best_height(self.single_profile, parent_hei, target_hei, parent_name, target_name,
                                     link_distance, 50, 50)

                else:
                    log_message(self.lst_log, 'Select a child of a site.')
            else:
                log_message(self.lst_log, 'No elevation profile found. Get it first')
        else:
            pass
        print('Optimize')

    def get_profile_all(self):
        self.single_profile = None  # borra el perfil del enlace sencillo
        self.all_profiles = None  # borra cualquier otra información de perfiles
        key = self.txt_api.text()  # la llave de la API
        log_message(self.lst_log, 'Fetching profiles...')
        if not key == '' and len(key) == 39:
            for starts, links in self.dict_links.items():
                for target, data in links.items():
                    if (target == 'lat' and isinstance(data, float)) or (target == 'lon' and isinstance(data, float))\
                            or (target == 'hei' and isinstance(data, float)):
                        continue
                    profile = get_profile(self.dict_links[starts]['lat'], self.dict_links[starts]['lon'],
                                          self.dict_links[starts][target][0], self.dict_links[starts][target][1],
                                          key)
                    self.dict_links[starts][target] = data + (profile,)
            filename = f'links-elevation-profile-{self.txt_fileprefix.text()}-out-threshold-{round(self.spn_distance.value()*1000)}-' \
                       f'{datetime.now().strftime("%d%m%y-%H%M%S")}.pickle'
            with open(os.path.join(self.parent.last_path, filename), 'wb') as file:
                pickle.dump(self.dict_links, file, protocol=pickle.HIGHEST_PROTOCOL)
                log_message(self.lst_log, f'created file {filename}')
            log_message(self.lst_log, 'Done fetching profiles')
            self.btn_optimize_heights.setEnabled(True)
            self.bnt_calculatelos_single.setEnabled(True)
            self.bnt_calculatelos_all.setEnabled(True)
            self.chk_images_all.setEnabled(True)
            self.chk_images_single.setEnabled(True)
            self.chk_alllos.setEnabled(True)
        else:
            log_message(self.lst_log, 'Please enter a correct API key of 39 characters')

    def get_profile(self):
        self.single_profile = None
        key = self.txt_api.text()
        log_message(self.lst_log, 'Fetching profiles...')
        if not key == '' and len(key) == 39:
            tree_line = self.tbl_linksmatrix.selectedItems()
            parent = tree_line[0].parent() if tree_line else None
            if parent:
                target_lat = tree_line[0].text(2)
                target_lon = tree_line[0].text(3)
                parent_lat = tree_line[0].parent().text(2)
                parent_lon = tree_line[0].parent().text(3)

                profile = get_profile(parent_lat, parent_lon, target_lat, target_lon, key, 100)

                self.single_profile = profile
                log_message(self.lst_log, 'Profile fetched')
                self.btn_optimize_heights.setEnabled(True)
                self.bnt_calculatelos_single.setEnabled(True)
                self.chk_images_single.setEnabled(True)
                self.chk_alllos.setEnabled(True)
            else:
                log_message(self.lst_log, 'Select a child of a site.')
        else:
            log_message(self.lst_log, 'Please enter a correct API key of 39 characters')

    def expand_table(self):
        if not self.table_expanded:  # table is contracted we need to expand
            self.tbl_linksmatrix.expandAll()
            self.table_expanded = True
        elif self.table_expanded:  # table is expanded we need to contract
            self.tbl_linksmatrix.collapseAll()
            self.table_expanded = False

    def load_los(self):
        file = open_dialog(self.parent, '(profiles *.pickle)', None)
        start_check = self.dict_links
        if file:
            with open(file[0], 'rb') as file:
                if not start_check:  # the loading is new
                    self.dict_links = pickle.load(file)
                else:  # we already have a self.dict. we just need to add the profiles loaded
                    temp_dict = pickle.load(file)
                    for site, connections in self.dict_links.items():
                        for element in connections:
                            if isinstance(self.dict_links[site][element], tuple):
                                self.dict_links[site][element] += (temp_dict[site][element][6],)
                    temp_dict = None
            if not start_check:  # there is nothing loaded we will recreate everything from the profile path
                self.populate_tree_widget()
                log_message(self.lst_log, 'Calculation matrix reconstructed from profile data. Loaded success.')
                log_message(self.lst_log, f'{len(self.dict_links)} sites connected')
            else:  # there was already calculated only send message that all was good
                log_message(self.lst_log, 'Profile file loaded')
            # activate extended controls
            self.btn_optimize_heights.setEnabled(True)
            self.bnt_getprofiles.setEnabled(True)
            self.bnt_getprofile.setEnabled(True)
            self.bnt_calculatelos_all.setEnabled(True)
            self.bnt_calculatelos_single.setEnabled(True)
            self.bnt_generatekml.setEnabled(True)
            self.chk_images_all.setEnabled(True)
            self.chk_images_single.setEnabled(True)
            self.chk_alllos.setEnabled(True)

    def calculate_los_all(self):
        timing_start = datetime.now()
        self.graph_book = []
        dict_links_copy = copy.deepcopy(self.dict_links)
        for start, links in self.dict_links.items():
            for target, data in links.items():
                if (target == 'lat' and isinstance(data, float)) or (target == 'lon' and isinstance(data, float)) \
                        or (target == 'hei' and isinstance(data, float)):
                    continue
                distance = round(data[3], 2)
                profile = data[6]
                if profile:
                    los, graph = check_los(profile, self.dict_links[start]['hei'], self.dict_links[start][target][2],
                                           start, target, distance, image=self.chk_images_all.isChecked())
                    # todo remove this line # we need to add another checkmark with and without LoS
                if not los[0][0]:
                    del dict_links_copy[start][target]
                    log_message(self.lst_log, f'removed link {target}')
                    if len(dict_links_copy[start]) < 4:
                        del dict_links_copy[start]
                        log_message(self.lst_log, f'removed site {start} it has no link')
                else:
                    if graph:
                        self.graph_book.append(graph)
        if self.chk_images_all.isChecked():
            file_name = f'LoS Data-{self.txt_fileprefix.text()}-out-threshold-' \
                        f'{round(self.spn_distance.value() * 1000)}-' \
                        f'{datetime.now().strftime("%d%m%y-%H%M%S")}.pdf'
            self.printpdf(os.path.join(self.parent.last_path, file_name), single=False)

        self.dict_links = dict_links_copy

        self.populate_tree_widget()
        timing_end = datetime.now() - timing_start
        message = f'tree updated - It took {timing_end}'
        log_message(self.lst_log, message)
        message = f'{len(self.dict_links)} / {self.targets} sites were connected'
        log_message(self.lst_log, message)

    def calculate_los(self):
        tree_line = self.tbl_linksmatrix.selectedItems()
        parent = tree_line[0].parent() if tree_line else None
        if parent:
            target = tree_line[0].text(1)
            start = parent.text(0)
            distance = tree_line[0].text(5)
            distance = float(distance[:distance.rfind(' km')])
            profile = self.dict_links[start][target][6]
            if profile:
                #  los is a tuple with 2 values 1 True/False if there is LoS. If True then 2 will have the graph
                    los = check_los(profile, self.dict_links[start]['hei'], self.dict_links[start][target][2],
                                    start, target, distance, image=self.chk_images_single.isChecked())
            if not los[0]:
                del self.dict_links[start][target]
                tree_list = tree_line[0].parent()
                tree_list.removeChild(tree_line[0])
                log_message(self.lst_log, f'removed link {target}')
                if len(self.dict_links[start]) < 4:
                    del self.dict_links[start]
                    root = self.tbl_linksmatrix.invisibleRootItem()
                    root.removeChild(tree_list)
                    log_message(self.lst_log, f'removed site {start} it has no links')
            else:
                if self.chk_images_single.isChecked():
                    file_name = f'Link {start} to {target} - {datetime.now().strftime("%d%m%y-%H%M%S")}.jpg'
                    self.printpdf(os.path.join(self.parent.last_path, file_name), single=True, graph=los[1])
        else:
            log_message(self.lst_log, 'Select a child of a site.')

    def printpdf(self, filename, single=True, graph=None):
        timing_start = datetime.now()
        if single:
            log_message(self.lst_log, 'Printing a single link')
            save_graph(filename, [graph], single=True)
        else:
            if self.graph_book:
                log_message(self.lst_log, 'Printing graphs to PDF...')
                save_graph(filename, self.graph_book, single=False)
            else:
                log_message(self.lst_log, 'The collection of LoS is empty. Has Calculate LoS(all) been run?')
        timing_end = datetime.now() - timing_start
        log_message(self.lst_log, f'Printed file: {filename}')
        log_message(self.lst_log, f'Printed in {timing_end}')

    def save_excel(self):
        timing_start = datetime.now()
        file_name = f'Link-matrix-out-{self.txt_fileprefix.text()}-out-threshold-' \
                    f'{round(self.spn_distance.value()*1000)}-' \
                    f'{datetime.now().strftime("%d%m%y-%H%M%S")}.csv'
        if self.dict_links:
            write_to_excel(self.dict_links, os.path.join(self.parent.last_path, file_name))
            timing_end = timing_start - datetime.now()
            log_message(self.lst_log, f'created file {file_name} in {timing_end}')
        else:
            log_message(self.lst_log, f'Error saving - No links matrix.')

    def load_pops(self):
        file_path = open_dialog(self.parent, '(*.xlsx *.csv)', multi_select=None)
        if file_path:
            self.txt_load_pops.setText(file_path[0][file_path[0].rfind('/')+1:])
            self.pops_f = file_path[0]

    def load_nodes(self):
        file_path = open_dialog(self.parent, '(*.xlsx *.csv)', multi_select=None)
        if file_path:
            self.txt_load_nodes.setText(file_path[0][file_path[0].rfind('/')+1:])
            self.sites_f = file_path[0]

    def calculate_matrix(self):
        self.lst_log.clear()
        self.tbl_linksmatrix.clear()
        if self.pops_f and self.sites_f:
            self.dict_links, self.all_sites, self.pops, self.targets = calculate_matrix(self.pops_f, self.sites_f,
                                                                                        self.spn_distance.value())

            self.populate_tree_widget()

            message = f'{len(self.dict_links)} / {self.targets} sites were connected'
            log_message(self.lst_log, message)
            # activate extended controls
            self.bnt_getprofiles.setEnabled(True)
            self.bnt_getprofile.setEnabled(True)
            self.bnt_generatekml.setEnabled(True)
        else:
            if self.pops_f:
                log_message(self.lst_log, 'Load a Nodes file.')
            if self.sites_f:
                log_message(self.lst_log, 'Load a Pops file.')
            else:
                log_message(self.lst_log, 'Load Pops and Nodes file.')

    def populate_tree_widget(self):
        tree_items = []
        for site, links in self.dict_links.items():
            site_item = QTreeWidgetItem([site, '', f'{self.dict_links[site]["lat"]}',
                                         f'{self.dict_links[site]["lon"]}', f'{self.dict_links[site]["hei"]}'])
            for target, link in links.items():
                if (target == 'lat' and isinstance(link, float)) or (target == 'lon' and isinstance(link, float)) \
                        or (target == 'hei' and isinstance(link, float)):
                    continue
                target_item = QTreeWidgetItem(['', target,
                                               f'{link[0]}', f'{link[1]}', f'{link[2]}',  # lat lon height
                                               f'{round(link[3], 2)} km',
                                               f'{round(link[4], 2)} °',
                                               f'{round(link[5], 2)} °'])
                site_item.addChild(target_item)
            tree_items.append(site_item)
        self.tbl_linksmatrix.insertTopLevelItems(0, tree_items)




