from bpy import context, data, ops

from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class ClearUtility:

    @staticmethod
    def clear_linked_libraries() -> None:
        for lib in data.libraries:
            data.batch_remove(ids=(lib,))

    @staticmethod
    def clear_materials() -> None:
        for material in data.materials:
            data.materials.remove(material)

    @staticmethod
    def clear_meshes() -> None:
        for mesh in data.meshes:
            data.meshes.remove(mesh)

    @staticmethod
    def clear_objects() -> None:
        for obj in context.scene.objects:
            obj.select_set(obj.type != 'CAMERA')

        ops.object.delete()

    @staticmethod
    def clear_collection(collection: str) -> None:
        time_tracker().start("clear_all", collection)
        logger().info("clear_all_for_collection - started: " + str(collection))

        if collection in data.collections.keys():
            objs_to_remove = list()
            collection_data = data.collections.get(collection)
            if collection_data is not None:
                for obj in collection_data.all_objects:
                    if obj.name in data.objects and obj.type != 'CAMERA':
                        objs_to_remove.append(obj)

            for obj in objs_to_remove:
                data.objects.remove(obj, do_unlink=True)

            data.collections.remove(data.collections[collection])

        time_tracker().end("clear_all", collection)

    @staticmethod
    def clear_all_collections() -> None:
        for collection in data.collections:
            ClearUtility.clear_collection(collection.name)

    @staticmethod
    def clear_all() -> None:
        time_tracker().start("clear_all")
        logger().info("clear_all - started")

        ClearUtility.clear_materials()
        ClearUtility.clear_objects()
        ClearUtility.clear_meshes()
        ClearUtility.clear_all_collections()
        ClearUtility.clear_linked_libraries()

        time_tracker().start("clear_all")
        stat_tracker().update_stat("clear_all")
