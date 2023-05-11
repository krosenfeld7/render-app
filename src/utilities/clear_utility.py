""" This utility class performs the clearing of old objects
    and data.
"""

from bpy import context, data, ops

from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class ClearUtility:
    """ This class provides a number of clearing operations.
        This assists with keeping memory usage down. """

    @staticmethod
    def clear_linked_libraries() -> None:
        """ Clears any linked libraries. """

        for lib in data.libraries:
            data.batch_remove(ids=(lib,))

    @staticmethod
    def clear_materials() -> None:
        """ Clears all materials. """

        for material in data.materials:
            data.materials.remove(material)

    @staticmethod
    def clear_meshes() -> None:
        """ Clears all meshes. """

        for mesh in data.meshes:
            data.meshes.remove(mesh)

    @staticmethod
    def clear_objects() -> None:
        """ Clears all objects except for the camera. """

        for obj in context.scene.objects:
            obj.select_set(obj.type != 'CAMERA')

        ops.object.delete()

    @staticmethod
    def clear_collection(collection: str) -> None:
        """ Clears all from a collection excluding the camera. """

        time_tracker().start("clear_all", collection)

        if collection in data.collections.keys():
            objs_to_remove = list()
            collection_data = data.collections.get(collection)
            if collection_data is not None:
                for obj in collection_data.all_objects:
                    if obj.name in data.objects and obj.type != 'CAMERA':
                        objs_to_remove.append(obj)

            # removal of objects needs to be performed
            # separately from the iteration above to
            # prevent an internal Blender crash
            for obj in objs_to_remove:
                data.objects.remove(obj, do_unlink=True)

            data.collections.remove(data.collections[collection])

        time_tracker().end("clear_all", collection)

    @staticmethod
    def clear_all_collections() -> None:
        """ Clears all collections. """

        for collection in data.collections:
            ClearUtility.clear_collection(collection.name)

    @staticmethod
    def clear_all() -> None:
        """ Clears everything from the scene. """

        time_tracker().start("clear_all")

        ClearUtility.clear_materials()
        ClearUtility.clear_objects()
        ClearUtility.clear_meshes()
        ClearUtility.clear_all_collections()
        ClearUtility.clear_linked_libraries()

        time_tracker().start("clear_all")
        stat_tracker().update_stat("clear_all")
