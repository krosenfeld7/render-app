from bpy import context, data
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
                node.inputs['Color'].default_value = \
                    background_settings.emission_color()
                node.inputs['Strength'].default_value = emission_value

    def set_hdri(self) -> None:
        background_settings = blender_settings().background_settings()
        node_env = self._world_scene.node_tree.nodes.new('ShaderNodeTexEnvironment')
        node_env.image = data.images.load(background_settings.hdri_path())
        node_env.location = -300, 0

        node_background = None
        for node in self._world_scene.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs['Strength'].default_value = 1.0
                node_background = node

        if node_background is not None:
            self._world_scene.node_tree.links.new(node_env.outputs['Color'],
                                                  node_background.inputs['Color'])


_instance = None


def world() -> World:
    global _instance
    if _instance is None:
        _instance = World()

    return _instance
