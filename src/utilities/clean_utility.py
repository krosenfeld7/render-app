""" This utility class assists with cleaning up file and component
    names so that they are usable by other classes.
"""

from os import path


class CleanUtility:
    """ This class provides basic cleaning operations
        for different components. """

    @staticmethod
    def clean_file_component(file: str) -> str:
        """ Cleans a file removing the path and an non-alphanumerics. """

        cleaned_component = path.splitext(path.basename(file))[0]
        return ''.join(filter(str.isalnum, cleaned_component)).lower()

    @staticmethod
    def clean_other_component(info: str) -> str:
        """ Cleans components. """

        return info.replace(" ", "").lower()

    @staticmethod
    def cleanup_file_components(file_components: list) -> list:
        """ Cleans all files. """

        return [CleanUtility.clean_file_component(component)
                for component in file_components]

    @staticmethod
    def cleanup_other_components(info_components: list) -> list:
        """ Cleans all other components. """

        return [CleanUtility.clean_other_component(component)
                for component in info_components]
