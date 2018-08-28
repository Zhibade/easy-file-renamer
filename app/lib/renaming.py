"""
Module containing the logic for all
file renaming of the application
"""

import logging
import os

from PySide2.QtCore import QThread, Signal

from app.utils import get_random_filename_in_dir


class FileRenameWorker(QThread):
    """
    Multi-threaded worker that handles all the
    file renaming process
    """

    aborted = Signal(str)


    def __init__(self, path, parent=None,
                 add_prefix=False, prefix="",
                 add_suffix=False, suffix="",
                 replace_name=False, old_name="", new_name=""):
        super(FileRenameWorker, self).__init__(parent)
        self.path = path

        self.add_prefix = add_prefix
        self.prefix = prefix

        self.add_suffix = add_suffix
        self.suffix = suffix

        self.old_name = old_name
        self.new_name = new_name
        self.rename = replace_name


    def run(self):
        """Overriding run method with custom logic"""

        try:
            norm_path = os.path.normpath(self.path)
            logging.info("Starting renaming on path: %s", norm_path)

            all_in_dir = os.listdir(norm_path)

            for dir_element in all_in_dir:
                full_path = os.path.join(norm_path, dir_element)

                if os.path.isfile(full_path):
                    file_name = os.path.basename(full_path)
                    final_name = full_rename(file_name,
                                             add_prefix=self.add_prefix, prefix=self.prefix,
                                             add_suffix=self.add_suffix, suffix=self.suffix,
                                             rename=self.rename, old_name=self.old_name, new_name=self.new_name)

                    os.rename(full_path, os.path.join(norm_path, final_name))

                    logging.info("Renamed %s to %s", dir_element, final_name)

        except OSError as error:
            logging.error("An error occurred while renaming: %s", error)
            self.aborted.emit(str(error))

        logging.info("End of renaming")


def full_rename(filename,
                add_prefix=False, prefix="",
                add_suffix=False, suffix="",
                rename=False, old_name="", new_name=""):
    """
    Does full renaming process (prefix, suffix, rename, extension)
    to passed filename according to passed arguments

    filename should be the filename with extension only, it doesn't support paths
    """

    new_filename = filename

    if rename:
        new_filename = get_new_file_name(new_filename, old_name, new_name)

    if add_prefix:
        new_filename = get_file_name_with_prefix(new_filename, prefix)

    if add_suffix:
        new_filename = get_file_name_with_suffix(new_filename, suffix)

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


def get_file_name_with_prefix(filename, prefix):
    """
    Returns the new file name by adding the provided prefix
    """

    new_name = "{0}{1}".format(prefix, filename)

    return new_name


def get_file_name_with_suffix(filename, suffix):
    """
    Returns the new file name by adding the provided suffix
    """

    ext_split = os.path.splitext(filename)

    new_name = "{0}{1}{2}".format(ext_split[0], suffix, ext_split[1])

    return new_name


cached_filename = ""
def get_preview_file_name(path,
                          add_prefix=False, prefix="",
                          add_suffix=False, suffix="",
                          rename=False, old_name="", new_name="", get_new=False):
    """
    Returns preview filename. When called for the first time it uses a random filename in
    the provided path and cache it. Every time after that it will use the cached filename
    unless [get_new] argument is set to True.

    If path is invalid, it returns an empty string.

    If there are no files in the provided path it returns "No files found"
    """

    global cached_filename

    norm_path = os.path.normpath(path)

    if not os.path.exists(norm_path):
        return "Invalid directory"

    if not get_new and cached_filename != "":
        return full_rename(cached_filename,
                           add_prefix=add_prefix, prefix=prefix,
                           add_suffix=add_suffix, suffix=suffix,
                           rename=rename, old_name=old_name, new_name=new_name)

    rand_filename = get_random_filename_in_dir(norm_path)

    if rand_filename is None:
        return "No files found"

    filename = full_rename(rand_filename,
                           add_prefix=add_prefix, prefix=prefix,
                           add_suffix=add_suffix, suffix=suffix,
                           rename=rename, old_name=old_name, new_name=new_name)
    cached_filename = filename

    return filename
