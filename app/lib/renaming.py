"""
Module containing the logic for all
file renaming of the application
"""

import os

from PySide2.QtCore import QThread, Signal


class FileRenameWorker(QThread):
    """
    Multi-threaded worker that handles all the
    file renaming process
    """
    aborted = Signal(str)
    finished = Signal()


    def __init__(self, path, parent=None, replace_name=False, old_name="", new_name=""):
        super(FileRenameWorker, self).__init__(parent)
        self.path = path
        self.old_name = old_name
        self.new_name = new_name
        self.rename = replace_name


    def run(self):
        """Overriding run method with custom logic"""

        try:
            norm_path = os.path.normpath(self.path)
            all_in_dir = os.listdir(norm_path)

            for dir_element in all_in_dir:
                full_path = os.path.join(norm_path, dir_element)

                if os.path.isfile(full_path):
                    file_name = os.path.basename(full_path)
                    final_name = full_rename(file_name, rename=self.rename,
                                             old_name=self.old_name, new_name=self.new_name)

                    os.rename(full_path, os.path.join(norm_path, final_name))

            self.finished.emit()

        except OSError as error:
            self.aborted.emit(str(error))


def full_rename(filename, rename=False, old_name="", new_name=""):
    """
    Does full renaming process (prefix, suffix, rename, extension)
    to passed filename according to passed arguments

    filename should be the filename with extension only, it doesn't support paths
    """

    new_filename = filename

    if rename:
        new_filename = get_new_file_name(new_filename, old_name, new_name)

    return new_filename


def get_new_file_name(filename, old_name, new_name):
    """
    Returns the new file name by replacing old_name with new_name
    filename should be the file name with extension only, without including directory

    It ignores the extension part when replacing.
    """

    ext_split = os.path.splitext(filename)

    new_name = ext_split[0].replace(old_name, new_name)

    return "{0}{1}".format(new_name, ext_split[1])
