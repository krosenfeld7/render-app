""" This module handles camera operations.
"""

from bpy import context, data, ops
from typing import Optional

from src.classes.exceptions import CameraNotFoundException
from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class Camera:
    """ This class provides a camera object that retains reference
        to the scene's camera and provides helpful camera operations. """

    def __init__(self,
                 camera_name='Camera',
                 scene_name='Scene') -> None:
        self._camera = data.objects[camera_name]
        self._camera_name = camera_name
        self._scene_name = scene_name

    def set_camera_to_perspective(self,
                                  perspective: bool) -> None:
        """ Sets the camera perspective. """

        self.set_camera_perspective('PERSP' if perspective else 'ORTHO')

    def set_camera_perspective(self,
                               perspective: str) -> None:
        """ Helper function for setting the camera perspective. """

        stat_tracker().update_stat("camera_persp", msg=perspective)
        self._camera.data.type = perspective

    def point_camera_at_origin(self) -> None:
        """ Points the camera at origin using some basic math. """

        if self._camera is None:
            raise CameraNotFoundException("No camera present in the scene")

        # camera points at origin at a distance of 10m
        self._camera.rotation_euler[0] = 0.0
        self._camera.rotation_euler[1] = 0.0
        self._camera.rotation_euler[2] = 0.0
        self._camera.location.x = 0.0
        self._camera.location.y = 0.0
        self._camera.location.z = 10.0
        self.set_camera_scene_resolution()

    def set_camera_scene_resolution(self) -> None:
        """ Sets the camera resolution based on the settings. """

        data.scenes[self._scene_name].render.resolution_x = blender_settings().render_settings().res_x()
        data.scenes[self._scene_name].render.resolution_y = blender_settings().render_settings().res_y()

    @staticmethod
    def align_camera_to_active_objects():
        """ Aligns the camera to ensure that all meshes are within the frame. """

        time_tracker().start("camera_align")

        objs_hide_from_render = list()
        # exclude all material meshes from view
        for collection in data.collections:
            if collection.name in app_settings().material_collection():
                for obj in collection.all_objects:
                    if obj.type == 'MESH':
                        objs_hide_from_render.append(obj)

        # hide all material objects from render
        for obj in objs_hide_from_render:
            obj.hide_render = True

        # deselect all material objects
        for obj in data.objects:
            obj.select_set(False)

        # select all other objects that are not hidden
        for obj in context.visible_objects:
            obj.select_set(not obj.hide_render)

        # perform alignment
        ops.view3d.camera_to_view_selected()

        # deselect all objects
        for obj in context.selected_objects:
            obj.select_set(False)

        stat_tracker().update_stat("camera_align")
        time_tracker().end("camera_align")


_instance = None


def camera(camera_name: Optional[str] = 'Camera',
           scene_name: Optional[str] = 'Scene') -> Camera:
    """ Singleton accessor for this class. """

    global _instance
    if _instance is None:
        _instance = Camera(camera_name, scene_name)

    return _instance
