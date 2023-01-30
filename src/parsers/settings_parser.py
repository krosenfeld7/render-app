from json import load
from typing import Optional

from src.classes.settings import AppSettings, BlenderSettings, TypeSettings


class SettingsParser:
    @staticmethod
    def parse(file_path: str) -> dict:
        with open(file_path, "r") as json_file:
            data = load(json_file)

        return data


app_settings_instance = None
blender_settings_instance = None
type_settings_instance = None


def app_settings(app_settings_path: Optional[str] = None) -> AppSettings:
    global app_settings_instance
    if app_settings_instance is None and app_settings_path is not None:
        app_settings_instance = \
            AppSettings(**SettingsParser.parse(app_settings_path))

    return app_settings_instance


def blender_settings(blender_settings_path: Optional[str] = None) -> BlenderSettings:
    global blender_settings_instance
    if blender_settings_instance is None and blender_settings_path is not None:
        blender_settings_instance = \
            BlenderSettings(**SettingsParser.parse(blender_settings_path))

    return blender_settings_instance


def type_settings(type_settings_path: Optional[str] = None) -> TypeSettings:
    global type_settings_instance
    if type_settings_instance is None and type_settings_path is not None:
        type_settings_instance = \
            TypeSettings(**SettingsParser.parse(type_settings_path))

    return type_settings_instance
