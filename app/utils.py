"""
Generic utilities module
"""

import os
import random


def ini_str_to_bool(value):
    """Converts string value retrieved from INI file to bool"""

    return True if value == "true" else False


def get_file_text(path):
    """Returns file contents as a single string"""

    contents = ""

    with open(path) as open_file:
        contents = ''.join(line.rstrip() for line in open_file)

    return contents


def get_random_filename_in_dir(path, include_subdir=False):
    """Returns the filename of a random file in the path"""

    if not os.path.exists(path):
        return ""

    dir_elements = []

    if include_subdir:
        for root, dirs, files in os.walk(path):
            for filename in files:
                dir_elements.append(filename)

        return random.choice(dir_elements)

    else:
        dir_elements = os.listdir(path)

        is_picking_file = True

        while is_picking_file:
            picked_file = random.choice(dir_elements)

            if os.path.isfile(os.path.join(path, picked_file)):
                return picked_file
