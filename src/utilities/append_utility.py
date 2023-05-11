""" This utility class is to assist with appending collections from
    Blender files.
"""

from bpy import data, ops

from src.classes.exceptions import CollectionNotFoundException
from src.parsers.settings_parser import app_settings
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class AppendUtility:
    """ This class provides the append functionality. """

    @staticmethod
    def append_from_file(file_path: str,
                         collection: str) -> None:
        time_tracker().start("append", collection)

        collection_path = file_path + \
            app_settings().paths().blender_collection()
        # append the collection to this file
        ops.wm.append(filename=collection,
                      directory=collection_path,
                      active_collection=False)

        stat_tracker().update_stat("append_for_collection", collection)
        time_tracker().end("append", collection)

        if collection not in data.collections.keys():
            # verify that the collection append was successful
            raise CollectionNotFoundException("Invalid Collection: '"
                                              + collection
                                              + "' not found in: '"
                                              + file_path)
