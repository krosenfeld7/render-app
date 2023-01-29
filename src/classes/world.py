from bpy import context
from typing import Any

from src.parsers.settings_parser import blender_settings


class World:

    def __init__(self) -> None:
        self._world_scene = context.scene.world

    def scene(self) -> Any:
        return self._world_scene

    def set_background_emission(self,
                                emission_value: float) -> None:
        background_settings = blender_settings().background_settings()
        for node in self._world_scene.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs[0].default_value = background_settings.emission_color()
                node.inputs[1].default_value = emission_value


_instance = None


def world() -> World:
    global _instance
    if _instance is None:
        _instance = World()

    return _instance
