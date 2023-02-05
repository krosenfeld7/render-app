from src.parsers.settings_parser import app_settings
from src.utilities.clean_utility import CleanUtility


class ValidationUtility:

    @staticmethod
    def validate_list(cleaner,
                      components: list,
                      collection: str) -> list:
        validated = list()
        for component in components:
            if app_settings().validate_entry(cleaner(component), collection):
                validated.append(component)

        return validated

    @staticmethod
    def validate_files(files: dict) -> dict:
        validated_files = dict()

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
        return ValidationUtility.validate_list(lambda component:
                                               CleanUtility.clean_other_component(component),
                                               components,
                                               collection)

    @staticmethod
    def validate_materials(materials: list) -> list:
        validated_material_names = ValidationUtility.validate_components([material.name
                                                                          for material in materials],
                                                                         app_settings().material_collection())
        return [material for material in materials if material.name in validated_material_names]
