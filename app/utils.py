"""
Generic utilities module
"""

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
