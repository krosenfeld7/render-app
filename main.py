""" This module provides the main start point for the app.
    Any GUI updates will be added and displayed via this module.

    Execution: python3 main.py
"""

from os import path, getcwd

from src.entry import execute


if __name__ == "__main__":
    # for now just call entry.py with the settings
    parameters = {'app_settings': "app_settings.json",
                  'blender_settings': "blender_settings.json",
                  'types': "types.json"}
    full_paths = dict()

    # compute paths for the settings files
    for entry in parameters:
        rel_path = path.join('config', parameters[entry])
        full_paths[entry] = path.join(getcwd(), rel_path)

    # call into the entry point
    execute(full_paths)
