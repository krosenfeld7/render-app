""" This utility class handles materials and related operations.
"""

from bpy import data
from typing import Any

from src.parsers.settings_parser import app_settings
from src.trackers.time_tracker import time_tracker
from src.utilities.append_utility import AppendUtility


class MaterialUtility:
    """ This class provides a number of material operations. """

    @staticmethod
    def aggregate_materials(material_collection: str) -> list:
        """ Finds all materials in the specified collection. """

        time_tracker().start("get_materials")

        materials = list()
        # retrieves all materials on meshes
        if material_collection in data.collections:
            for obj in data.collections[material_collection].all_objects:
                if obj.type == 'MESH':
                    materials.extend(obj.data.materials)

        time_tracker().end("get_materials")
        return materials

    @staticmethod
    def update_meshes_with_material(meshes: set,
                                    target_material: Any) -> None:
        """ Updates the provides meshes with the target material. """

        time_tracker().start("update_meshes")

        for mesh in meshes:
            # clear all previous materials and add this new material
            mesh.data.materials.clear()
            mesh.data.materials.append(target_material)

        time_tracker().end("update_meshes")

    @staticmethod
    def get_materials(files: dict) -> list:
        """ Gets all of the materials specified. """

        # retrieve all materials from all files in the materials collection
        for file in files[app_settings().material_collection()]:
            AppendUtility.append_from_file(
                file,
                app_settings().material_collection()
            )

        # find all of the specific materials across all objects
        return MaterialUtility.aggregate_materials(
            app_settings().material_collection()
        )

    @staticmethod
    def get_immaterial_collections() -> list:
        """ Finds all collections that are not specified as material collections. """

        collections = sorted(app_settings().collections().keys())
        non_material_collections_by_priority = list()
        for collection in collections:
            if app_settings().collections()[collection] \
                    not in app_settings().material_collection():
                non_material_collections_by_priority.append(
                    app_settings().collections()[collection]
                )

        return non_material_collections_by_priority
