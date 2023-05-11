""" This module handles directory parsing.
"""

from os import path, listdir

from src.parsers.settings_parser import app_settings


class DirectoryParser:
    """ This class performs the parsing of the search directory
        and finds the necessary files. """

    def __init__(self,
                 root_dir: str,
                 directories: list,
                 file_extension: str) -> None:
        self._root_dir = root_dir
        self._directories = directories
        self._file_extension = file_extension

    def parse(self) -> dict:
        """ Performs the parsing of the directories provided,
            taking into account the path and extension. """

        # Simple walking of directories, returning each of the files
        # Stores the valid files according to their collection type (directory name)
        files_by_directories = dict()
        for directory in self._directories:
            dir_path = path.join(self._root_dir, directory)
            directory_list = list()
            for file_name in listdir(dir_path):
                file_path = path.join(dir_path, file_name)
                if path.isfile(file_path) and \
                        file_path.endswith(self._file_extension):
                    directory_list.append(file_path)

            files_by_directories[directory] = sorted(directory_list)

        return files_by_directories


def parse_directories() -> dict:
    """ Simple accessor for this class. Returns the valid files by
        collection type. """

    root_dir = app_settings().paths().search_dir_path()
    directories = list(app_settings().collections().values())
    file_extension = app_settings().paths().blender_file_extension()
    # pass settings to the parser and return parsed result
    return DirectoryParser(root_dir, directories, file_extension).parse()
