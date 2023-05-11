""" This module provides an entry point into the Blender subprocess. This code
    pulls the necessary information from the settings files
    and executes Blender.
"""

from os import getcwd, path
from subprocess import run

from src.parsers.settings_parser import app_settings


def execute(parameters: dict) -> None:
    """ Extracts the necessary settings then executes Blender in
        a subprocess. """
    app_settings(parameters['app_settings'])
    path_settings = app_settings().paths()

    blender_exe = path_settings.blender_exe()
    blend_file = path.join(getcwd(), path_settings.main_file())
    driver = path.join(getcwd(), path_settings.driver())

    run([blender_exe, "-b", "--python", driver, blend_file, "--", *parameters.values()])
