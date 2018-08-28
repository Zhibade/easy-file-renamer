"""
Module containing main GUI for the application
"""

import os

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox

from app.lib.renaming import FileRenameWorker, get_preview_file_name
from app.ui.ui_main_dialog import UIMainDialog
from app.utils import ini_str_to_bool
from app.constants import LOG_FILE_PATH


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
        self.file_renamer_worker = None
        self.settings = QSettings(QSettings.IniFormat,
                                  QSettings.UserScope,
                                  SETTINGS_LABEL,
                                  SETTINGS_LABEL)

        self.init_signals()
        self.load_settings()
        self.update_line_edits()


    def browse_path(self):
        """
        Displays directory browser and sets the path line edit
        if a directory is chosen
        """

        path = QFileDialog.getExistingDirectory(caption="Select directory")

        if path != "":
            self.target_path_line_edit.setText(path)


    def init_renaming(self):
        """
        Starts renaming process.
        It checks the path before attempting to rename
        """

        path = self.target_path_line_edit.text()
        is_valid_path = os.path.isdir(path)

        if not is_valid_path:
            QMessageBox.warning(self, "EasyFileRenamer - Warning",
                                "Invalid directory specified. Please select an existing directory")
            return

        proceed = QMessageBox.question(self, "EasyFileRenamer - Warning",
                                       ("This operation cannot be undone."
                                        "\n\nDo you wish to continue?"),
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if proceed == QMessageBox.No:
            return

        self.rename_files_btn.setEnabled(False)

        should_add_prefix = self.prefix_chk.isChecked()
        prefix = self.prefix_line_edit.text()

        should_add_suffix = self.suff_chk.isChecked()
        suffix = self.suff_line_edit.text()

        should_rename = self.rename_chk.isChecked()
        old_name = self.rename_old_line_edit.text()
        new_name = self.rename_new_line_edit.text()

        self.file_renamer_worker = FileRenameWorker(path,
                                                    add_prefix=should_add_prefix, prefix=prefix,
                                                    add_suffix=should_add_suffix, suffix=suffix,
                                                    replace_name=should_rename, old_name=old_name, new_name=new_name)
        self.file_renamer_worker.aborted.connect(self.renaming_aborted)
        self.file_renamer_worker.finished.connect(self.renaming_finished)

        self.file_renamer_worker.start()


    def init_signals(self):
        """Connects widgets' signals to their callbacks"""

        self.finished.connect(self.save_settings)

        self.prefix_chk.stateChanged.connect(self.update_line_edits)
        self.suff_chk.stateChanged.connect(self.update_line_edits)
        self.ext_chk.stateChanged.connect(self.update_line_edits)
        self.rename_chk.stateChanged.connect(self.update_line_edits)

        self.browse_path_btn.clicked.connect(self.browse_path)
        self.rename_files_btn.clicked.connect(self.init_renaming)
        self.view_log_btn.clicked.connect(self.open_log_file)

        self.target_path_line_edit.textChanged.connect(lambda: self.update_preview_label(force_new=True))
        self.prefix_line_edit.textChanged.connect(lambda: self.update_preview_label())
        self.suff_line_edit.textChanged.connect(lambda: self.update_preview_label())
        self.rename_old_line_edit.textChanged.connect(lambda: self.update_preview_label())
        self.rename_new_line_edit.textChanged.connect(lambda: self.update_preview_label())


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


    def open_log_file(self):
        """Opens log file in the system's default application"""

        os.startfile(LOG_FILE_PATH)


    def renaming_aborted(self, error):
        """Displays error message if renaming fails"""

        QMessageBox.critical(self, "EasyFileRenamer - Error", error)


    def renaming_finished(self):
        """Updates UI and displays a message when renaming is finished"""

        self.rename_files_btn.setEnabled(True)
        QMessageBox.information(self, "EasyFileRenamer - Success!", "Renamed files successfully!")


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

        self.update_preview_label()


    def update_preview_label(self, force_new=False):
        """Updates preview file using the provided path and line edit values"""

        path = self.target_path_line_edit.text()

        should_add_prefix = self.prefix_chk.isChecked()
        prefix = self.prefix_line_edit.text()

        should_add_suffix = self.suff_chk.isChecked()
        suffix = self.suff_line_edit.text()

        should_rename = self.rename_chk.isChecked()
        old_name = self.rename_old_line_edit.text()
        new_name = self.rename_new_line_edit.text()

        preview_filename = get_preview_file_name(path,
                                                 add_prefix=should_add_prefix, prefix=prefix,
                                                 add_suffix=should_add_suffix, suffix=suffix,
                                                 rename=should_rename, old_name=old_name, new_name=new_name,
                                                 get_new=force_new)

        self.prev_file_name_label.setText(preview_filename)
