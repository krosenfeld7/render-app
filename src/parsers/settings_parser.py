""" This module handles settings parsing.
"""

from json import load
from typing import Optional

from src.classes.settings import AppSettings, BlenderSettings, TypeSettings


class SettingsParser:
    """ This class parses the configuration files and stores the results
        in the corresponding settings type. """

    @staticmethod
    def parse(file_path: str) -> dict:
        """ Performs parsing of the json settings file. """

        with open(file_path, "r") as json_file:
            data = load(json_file)

        return data


app_settings_instance = None
blender_settings_instance = None
type_settings_instance = None


def app_settings(app_settings_path: Optional[str] = None) -> AppSettings:
    """ Singleton accessor that uses dictionary expansion to store each
        app settings field into it's respective object. """

    global app_settings_instance
    if app_settings_instance is None and app_settings_path is not None:
        app_settings_instance = \
            AppSettings(**SettingsParser.parse(app_settings_path))

    return app_settings_instance


def blender_settings(blender_settings_path: Optional[str] = None) -> BlenderSettings:
    """ Singleton accessor that uses dictionary expansion to store each
        blender settings field into it's respective object. """

    global blender_settings_instance
    if blender_settings_instance is None and blender_settings_path is not None:
        blender_settings_instance = \
            BlenderSettings(**SettingsParser.parse(blender_settings_path))

    return blender_settings_instance


def type_settings(type_settings_path: Optional[str] = None) -> TypeSettings:
    """ Singleton accessor that uses dictionary expansion to store each
        type settings field into it's respective object. """

    global type_settings_instance
    if type_settings_instance is None and type_settings_path is not None:
        type_settings_instance = \
            TypeSettings(**SettingsParser.parse(type_settings_path))

    return type_settings_instance
