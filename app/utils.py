"""
Generic utilities module
"""

def get_file_text(path):
    """
    Returns file contents as a single string
    """

    contents = ""

    with open(path) as f:
        contents = ''.join(line.rstrip() for line in f)

    return contents
