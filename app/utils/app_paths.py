import os
import sys


def get_app_data_dir():
    base = os.getenv("LOCALAPPDATA")  # Windows padrão

    app_dir = os.path.join(base, "TranscriberPipeline")

    os.makedirs(app_dir, exist_ok=True)

    return app_dir


def get_output_dir():
    path = os.path.join(get_app_data_dir(), "output")
    os.makedirs(path, exist_ok=True)
    return path


def get_temp_dir():
    path = os.path.join(get_app_data_dir(), "temp")
    os.makedirs(path, exist_ok=True)
    return path