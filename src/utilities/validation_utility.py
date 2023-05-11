""" This utility class handles validation of a number of different
    objects and types that are used throughout the app.
"""

from src.parsers.settings_parser import app_settings
from src.utilities.clean_utility import CleanUtility


class ValidationUtility:
    """ This class provides validation operations. """

    @staticmethod
    def validate_list(cleaner,
                      components: list,
                      collection: str) -> list:
        """ Validates provided components and collection. """

        validated = list()
        for component in components:
            # validates against the blacklist/whitelist
            if app_settings().validate_entry(cleaner(component), collection):
                validated.append(component)

        return validated

    @staticmethod
    def validate_files(files: dict) -> dict:
        """ Validates each of the files provided. """

        validated_files = dict()

        # cleans the file names for comparison against the blacklist/whitelist
        for directory, file_list in files.items():
            validated_files[directory] = \
                ValidationUtility.validate_list(lambda file:
                                                CleanUtility.clean_file_component(file),
                                                file_list,
                                                directory)
        return validated_files

    @staticmethod
    def validate_components(components: list,
                            collection: str) -> list:
        """ Validates each of the components provided for the specified collection. """

        # cleans the components for comparison against the blacklist/whitelist
        return ValidationUtility.validate_list(lambda component:
                                               CleanUtility.clean_other_component(component),
                                               components,
                                               collection)

    @staticmethod
    def validate_materials(materials: list) -> list:
        """ Validates each material in the list. """

        validated_material_names = ValidationUtility.validate_components(
            [material.name for material in materials],
            app_settings().material_collection()
        )

        return [material for material in materials
                if material.name in validated_material_names]
