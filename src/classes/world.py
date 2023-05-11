""" This module handles world object related operations.
"""

from bpy import context, data
from typing import Any

from src.parsers.settings_parser import blender_settings


# noinspection SpellCheckingInspection
class World:
    """ This class provides a world object that retains reference
        to the scene's world and provides helpful world operations. """

    def __init__(self) -> None:
        self._world_scene = context.scene.world

    def scene(self) -> Any:
        """ Returns this world's scene. """

        return self._world_scene

    def set_background_emission(self,
                                emission_value: float) -> None:
        """ Sets this world's background emission. """

        background_settings = blender_settings().background_settings()
        for node in self._world_scene.node_tree.nodes:
            # we only want to update the nodes that are
            # actually the background
            if node.type == 'BACKGROUND':
                # we set the color and strength for good measure
                node.inputs['Color'].default_value = \
                    background_settings.emission_color()
                node.inputs['Strength'].default_value = emission_value

    def set_hdri(self,
                 hdri_path: str) -> None:
        """ Sets this world's hdri. """

        # creates the new hdri node
        node_env = \
            self._world_scene.node_tree.nodes.new('ShaderNodeTexEnvironment')
        node_env.image = data.images.load(hdri_path)
        node_env.location = -300, 0

        node_background = None
        # find the appropriate background node
        for node in self._world_scene.node_tree.nodes:
            if node.type == 'BACKGROUND':
                node.inputs['Strength'].default_value = 1.0
                node_background = node

        if node_background is not None:
            # link the hdri node to the background
            self._world_scene.node_tree.links.new(
                node_env.outputs['Color'],
                node_background.inputs['Color']
            )


_instance = None


def world() -> World:
    """ Singleton accessor for this class. """

    global _instance
    if _instance is None:
        _instance = World()

    return _instance
