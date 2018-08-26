"""
Generic utilities module
"""

import os


def ini_str_to_bool(value):
    """Converts string value retrieved from INI file to bool"""

    return True if value == "true" else False


def get_file_text(path):
    """
    Returns file contents as a single string
    """

    contents = ""

    with open(path) as open_file:
        contents = ''.join(line.rstrip() for line in open_file)

    return contents


def get_new_file_name(filename, old_name, new_name):
    """
    Returns the new file name by replacing old_name with new_name
    filename should be the file name with extension only, without including directory

    It ignores the extension part when replacing.
    """

    ext_split = os.path.splitext(filename)
    new_name = ext_split[0].replace(old_name, new_name)

    return "{0}{1}".format(new_name, ext_split[1])
