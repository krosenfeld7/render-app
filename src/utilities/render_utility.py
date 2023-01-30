from os import path, makedirs
from bpy import context, ops

from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class RenderUtility:

    @staticmethod
    def file_name_for_components(file_components: list) -> str:
        file_name = '_'.join(file_components)
        file_name += '.' + blender_settings().image_settings().file_format().lower()
        file_path = path.join(app_settings().paths().output_dir_path(), file_name)

        if not path.exists(app_settings().paths().output_dir_path()):
            makedirs(app_settings().paths().output_dir_path())

        return file_path

    @staticmethod
    def render_file(file_components: list) -> None:
        time_tracker().start("render")
        file_name = RenderUtility.file_name_for_components(file_components)
        if path.exists(file_name) and not app_settings().parameters().overwrite():
            logger().info("Already exists, skipping: " + file_name)
            return

        context.scene.render.filepath = file_name
        ops.render.render(write_still=True)

        stat_tracker().update_stat("render")
        time_tracker().end("render")
