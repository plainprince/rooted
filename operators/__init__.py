import os


def get_addon_filepath():
    """
    Returns the absolute path to the add-on's root directory.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


classes = []

