""" This utility class handles meshes and related operations.
"""

from bpy import data
from typing import Any

from src.parsers.settings_parser import app_settings
from src.trackers.time_tracker import time_tracker


class MeshUtility:
    """ This class provides a number of mesh operations. """

    @staticmethod
    def meshes_in_collection(collection: Any) -> set:
        """ Returns all meshes in a collection. """

        meshes = set()
        for obj in collection.all_objects:
            if obj.type == 'MESH':
                meshes.add(obj)

        return meshes

    @staticmethod
    def all_meshes_in_scene() -> set:
        """ Returns all non material meshes in the scene. """

        time_tracker().start("get_meshes")

        meshes = set()
        for collection in data.collections:
            # exclude meshes that are in the material collection
            if collection.name not in app_settings().material_collection():
                meshes.update(MeshUtility.meshes_in_collection(collection))

        time_tracker().end("get_meshes")
        return meshes

    @staticmethod
    def all_meshes_in_collection(collection_name: str) -> set:
        """ Returns all meshes in the specified collection. """

        time_tracker().start("get_meshes")
        meshes = set()
        for collection in data.collections:
            if collection.name == collection_name:
                meshes.update(MeshUtility.meshes_in_collection(collection))

        time_tracker().end("get_meshes")
        return meshes
