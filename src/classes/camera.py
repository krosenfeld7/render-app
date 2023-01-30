from bpy import context, data, ops
from typing import Optional

from src.classes.exceptions import CameraNotFoundException
from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class Camera:

    def __init__(self,
                 camera_name='Camera',
                 scene_name='Scene') -> None:
        self._camera = data.objects[camera_name]
        self._camera_name = camera_name
        #self._camera_perspective = self._camera.data.type
        self._scene_name = scene_name

    def set_camera_to_perspective(self,
                                  perspective: bool) -> None:
        self.set_camera_perspective('PERSP' if perspective else 'ORTHO')

    def set_camera_perspective(self,
                               perspective: str) -> None:
        #if perspective != self._camera.data.type:
        stat_tracker().update_stat("camera_persp", msg=perspective)
        self._camera.data.type = perspective
        # TODO: ENSURE THIS WORKS
        """
        for obj in context.scene.objects:
            if obj is not None and obj.type == 'CAMERA':
                if perspective:
                    obj.data.type = 'PERSP'
                else:
                    obj.data.type = 'ORTHO'
                prev_camera_perspective = obj.data.type
        """

    def point_camera_at_origin(self) -> None:
        if self._camera is None:
            raise CameraNotFoundException("No camera present in the scene")

        self._camera.rotation_euler[0] = 0.0
        self._camera.rotation_euler[1] = 0.0
        self._camera.rotation_euler[2] = 0.0
        self._camera.location.x = 0.0
        self._camera.location.y = 0.0
        self._camera.location.z = 10.0
        self.set_camera_scene_resolution()

    def set_camera_scene_resolution(self) -> None:
        data.scenes[self._scene_name].render.resolution_x = blender_settings().render_settings().res_x()
        data.scenes[self._scene_name].render.resolution_y = blender_settings().render_settings().res_y()

    @staticmethod
    def align_camera_to_active_objects():
        time_tracker().start("camera_align")

        objs_hide_from_render = list()
        for collection in data.collections:
            if collection.name in app_settings().material_collection():
                for obj in collection.all_objects:
                    if obj.type == 'MESH':
                        objs_hide_from_render.append(obj)

        for obj in objs_hide_from_render:
            obj.hide_render = True

        for obj in data.objects:
            obj.select_set(False)

        for obj in context.visible_objects:
            obj.select_set(not obj.hide_render)

        ops.view3d.camera_to_view_selected()

        for obj in context.selected_objects:
            obj.select_set(False)

        stat_tracker().update_stat("camera_align")
        time_tracker().end("camera_align")


_instance = None


def camera(camera_name: Optional[str] = 'Camera',
           scene_name: Optional[str] = 'Scene') -> Camera:
    global _instance
    if _instance is None:
        _instance = Camera(camera_name, scene_name)

    return _instance
