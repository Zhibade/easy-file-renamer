"""
Module containing main GUI for the application
"""

from PySide2.QtWidgets import QDialog

from app.ui.ui_main_dialog import UIMainDialog


class GUI(QDialog, UIMainDialog):
    """
    Main GUI for the application
    """

    def __init__(self, parent = None):
        super(GUI, self).__init__(parent)
        self.setup_ui(self)
