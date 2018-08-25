"""
Module containing main GUI for the application
"""

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QDialog

from app.ui.ui_main_dialog import UIMainDialog
from app.utils import ini_str_to_bool


# Constants

SETTING_ADD_PREFIX = 'add_prefix'
SETTING_ADD_PREFIX_DEFAULT = False

SETTING_ADD_SUFFIX = 'add_suffix'
SETTING_ADD_SUFFIX_DEFAULT = False

SETTING_CHANGE_EXT = 'change_ext'
SETTING_CHANGE_EXT_DEFAULT = False

SETTING_INCLUDE_SUBDIR = 'include_subdir'
SETTING_INCLUDE_SUBDIR_DEFAULT = False

SETTING_RENAME = 'rename'
SETTING_RENAME_DEFAULT = True

SETTINGS_LABEL = "EasyFileRenamer"


class GUI(QDialog, UIMainDialog):
    """
    Main GUI for the application
    """

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setup_ui(self)
        self.settings = QSettings(QSettings.IniFormat,
                                  QSettings.UserScope,
                                  SETTINGS_LABEL,
                                  SETTINGS_LABEL)

        self.init_signals()
        self.load_settings()
        self.update_line_edits()


    def init_signals(self):
        """Connects widgets' signals to their callbacks"""

        self.finished.connect(self.save_settings)

        self.prefix_chk.stateChanged.connect(self.update_line_edits)
        self.suff_chk.stateChanged.connect(self.update_line_edits)
        self.ext_chk.stateChanged.connect(self.update_line_edits)
        self.rename_chk.stateChanged.connect(self.update_line_edits)


    def load_settings(self):
        """Loads initial settings from INI file for the UI widgets"""

        prefix_value = self.settings.value(SETTING_ADD_PREFIX, SETTING_ADD_PREFIX_DEFAULT)
        suff_value = self.settings.value(SETTING_ADD_SUFFIX, SETTING_ADD_SUFFIX_DEFAULT)
        ext_value = self.settings.value(SETTING_CHANGE_EXT, SETTING_CHANGE_EXT_DEFAULT)
        subdir_value = self.settings.value(SETTING_INCLUDE_SUBDIR, SETTING_INCLUDE_SUBDIR_DEFAULT)
        rename_value = self.settings.value(SETTING_RENAME, SETTING_RENAME_DEFAULT)

        self.prefix_chk.setChecked(ini_str_to_bool(prefix_value))
        self.suff_chk.setChecked(ini_str_to_bool(suff_value))
        self.ext_chk.setChecked(ini_str_to_bool(ext_value))
        self.include_subdir_chk.setChecked(ini_str_to_bool(subdir_value))
        self.rename_chk.setChecked(ini_str_to_bool(rename_value))


    def save_settings(self):
        """Saves UI checkboxes settings to settings file"""

        self.settings.setValue(SETTING_ADD_PREFIX, self.prefix_chk.isChecked())
        self.settings.setValue(SETTING_ADD_SUFFIX, self.suff_chk.isChecked())
        self.settings.setValue(SETTING_CHANGE_EXT, self.ext_chk.isChecked())
        self.settings.setValue(SETTING_INCLUDE_SUBDIR, self.include_subdir_chk.isChecked())
        self.settings.setValue(SETTING_RENAME, self.rename_chk.isChecked())


    def update_line_edits(self):
        """Updates line edits based on their corresponding checkboxes values"""

        self.prefix_line_edit.setEnabled(self.prefix_chk.isChecked())
        self.suff_line_edit.setEnabled(self.suff_chk.isChecked())
        self.ext_line_edit.setEnabled(self.ext_chk.isChecked())
        self.rename_old_line_edit.setEnabled(self.rename_chk.isChecked())
        self.rename_new_line_edit.setEnabled(self.rename_chk.isChecked())
