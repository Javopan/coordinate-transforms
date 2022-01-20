from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem


def define_action(icon, name, tooltip, trigger, shortcut=None, parent=None):
    """
    Defines an action to the toolbar
    :param shortcut: str, shortcut that we want to use, e.g. "Ctrl+o"
    :param icon: str, path to an icon file e.g. icons/open.svg
    :param name: str, name of the action e.g. Open...
    :param tooltip: str, tooltip of the action e.g. opens a file
    :param trigger: function, function that the action will trigger e.g. open_file (withoout the ())
    :param parent: object, parent of the action
    :return: object, returns a pyqt action
    """
    # Open action
    if icon is not None:  # if we have a icon
        action = QAction(QIcon(icon), name, parent)  # Creates the Action
    else:  # create the action without icon. Prints the name
        action = QAction(name, parent)
    action.setToolTip(tooltip)  # Sets a tooltip
    action.setStatusTip(action.toolTip())  # Sets the tooltip to the status bar
    action.triggered.connect(trigger)  # What the action triggers

    if shortcut:
        action.setShortcut(QKeySequence(shortcut))

    return action


def open_dialog(parent, filter_, multi_select=None):
    if multi_select:
        pass
    else:
        dlg_open = QFileDialog(caption=f'Open file for {parent.apps[parent.appowner]}', filter=f'Sites files {filter_}',
                               directory=parent.last_path)
        dlg_open.exec()
        n_files = len(dlg_open.selectedFiles())
        files = dlg_open.selectedFiles()

    if files:
        parent.last_path = files[0][:files[0].rfind('/')]
    return files


def log_message(log_widget, message):
    message_item = QListWidgetItem(message)
    log_widget.insertItem(0, message_item)
