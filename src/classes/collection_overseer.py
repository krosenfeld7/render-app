""" This module handles collection operations.
"""

from src.classes.exceptions import InvalidFileException
from src.classes.overseer import Overseer
from src.utilities.append_utility import AppendUtility
from src.utilities.clear_utility import ClearUtility
from src.utilities.clean_utility import CleanUtility


class CollectionOverseer(Overseer):
    """ This class provides the overseer for collections.
        This is used to encapsulate collections with a simple interface. """

    def __init__(self,
                 repeat: int,
                 collection: str,
                 files=None) -> None:
        super(CollectionOverseer, self).__init__(repeat)
        self._collection = collection
        self._files = files
        self._names = CleanUtility.cleanup_file_components(files)
        self._file_index = 0

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state.
            This overseer handles collection operations. """

        # ensure that we are using a valid file
        if self._file_index >= len(self._files):
            raise InvalidFileException("Hit a file index that "
                                       "is out of the valid range: "
                                       + str(self._file_index) + ", max: "
                                       + str(len(self._files))
                                       + ", for collection: " + self._collection)

        # only perform the update when required
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        # begin by clearing the old objects for the collection
        ClearUtility.clear_collection(self._collection)
        # use the append utility to retrieve the new collection's objects
        AppendUtility.append_from_file(self._files[self._file_index],
                                       self._collection)
        self._file_index += 1
        self._file_index %= len(self._files)

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. This is equivalent
            to the number of files in this collection. """

        return len(self._files)

    def __str__(self):
        # the currently appended file is one before the index tracker
        currently_appended_index = self._file_index - 1
        currently_appended_index %= len(self._files)
        return str(self._names[currently_appended_index])


def collection_dispatcher(*args, **kwargs) -> CollectionOverseer:
    """ Provides dispatch access to the CollectionOverseer type.
        This is necessary to provide generic Overseer dispatching. """

    return CollectionOverseer(*args, **kwargs)
