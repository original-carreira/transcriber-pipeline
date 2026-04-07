import sys
import os


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS

    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )


def get_resource_path(relative_path: str) -> str:
    return os.path.abspath(
        os.path.join(get_base_path(), relative_path)
    )