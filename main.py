"""
This application allows the user to rename and add prefix, and suffix to
multiple files easily.

Small Qt application made for learning purposes
"""

import logging
import sys

from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication

from app.ui.main_gui import GUI
from app.constants import LOG_FILE_PATH


__appname__ = "Easy File Renamer"
__module__ = "main"

__author__ = "Jose Ivan Lopez Romo"
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "lopezromo.jose@gmail.com"


if __name__ == "__main__":
    logging.basicConfig(handlers=[logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')],
                        level=logging.INFO, format="%(asctime)s -- %(levelname)s -- %(message)s")

    QCoreApplication.setApplicationName("EasyFileRenamer")
    QCoreApplication.setApplicationVersion("1.0")
    QCoreApplication.setOrganizationName("EasyFileRenamer")
    QCoreApplication.setOrganizationDomain("www.ivanlopezr.com")

    logging.info("--- APPLICATION STARTED ---")

    QApplication.setStyle("fusion")
    app = QApplication(sys.argv)

    form = GUI()
    form.show()

    sys.exit(app.exec_())
