from bpy import data

from src.parsers.settings_parser import app_settings
from src.trackers.logger import logger
from src.trackers.time_tracker import time_tracker


class MeshUtility:

    @staticmethod
    def cleanup_non_meshes(collection: str) -> None:
        if collection in data.collections.keys():
            for obj in data.collections[collection].all_objects:
                if obj is not None and obj.type != 'MESH':
                    curve = obj.data
                    data.objects.remove(obj, do_unlink=True)
                    data.curves.remove(curve)
        else:
            logger().error("cleanup_non_meshes - invalid collection: " + collection)

    @staticmethod
    def all_meshes_in_scene() -> set:
        time_tracker().start("get_meshes")

        meshes = set()
        for collection in data.collections:
            if collection.name not in app_settings().material_collection():
                for obj in collection.all_objects:
                    if obj.type == 'MESH':
                        meshes.add(obj)

        time_tracker().end("get_meshes")
        return meshes
