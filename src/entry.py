from subprocess import run

import os

from src.parsers.settings_parser import app_settings


def execute(parameters: dict) -> None:
    app_settings(parameters['app_settings'])
    path_settings = app_settings().paths()

    blender_exe = path_settings.blender_exe()
    blend_file = os.path.join(os.getcwd(), path_settings.main_file())
    driver = os.path.join(os.getcwd(), path_settings.driver())

    run([blender_exe, "--python", driver, blend_file, "--", *parameters.values()])
