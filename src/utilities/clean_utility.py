from os import path


class CleanUtility:
    @staticmethod
    def clean_file_component(file: str) -> str:
        cleaned_component = path.splitext(path.basename(file))[0]
        return ''.join(filter(str.isalnum, cleaned_component)).lower()

    @staticmethod
    def clean_other_component(info: str) -> str:
        return info.replace(" ", "").lower()

    @staticmethod
    def cleanup_file_components(file_components: list) -> list:
        return [CleanUtility.clean_file_component(component) for component in file_components]

    @staticmethod
    def cleanup_other_components(info_components: list) -> list:
        return [CleanUtility.clean_other_component(component) for component in info_components]
