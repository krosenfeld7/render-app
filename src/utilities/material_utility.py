from bpy import data
from typing import Any

from src.trackers.logger import logger
from src.trackers.time_tracker import time_tracker


class MaterialUtility:

    @staticmethod
    def get_materials(material_collections: list) -> list:
        time_tracker().start("get_materials")
        logger().info("get_target_materials - started")

        materials = list()
        for material_collection in material_collections:
            if material_collection in data.collections:
                for obj in data.collections[material_collection].all_objects:
                    if obj.type == 'MESH':
                        materials.extend(obj.data.materials)

        time_tracker().end("get_materials")
        return materials

    @staticmethod
    def update_meshes_with_material(meshes: set,
                                    target_material: Any) -> None:
        time_tracker().start("update_meshes")
        logger().info("update_all_meshes_with_material - started: " + str(target_material.name))

        for mesh in meshes:
            mesh.data.materials.clear()
            mesh.data.materials.append(target_material)

        time_tracker().end("update_meshes")
