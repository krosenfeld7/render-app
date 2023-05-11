""" This utility class handles rendering and related operations.
"""

from bpy import context, ops
from os import path, makedirs

from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class RenderUtility:
    """ This class provides render operations. """

    @staticmethod
    def file_name_for_components(file_components: list) -> str:
        """ Returns a file name for the provided components. """

        file_name = '_'.join(file_components)
        file_name += '.' + blender_settings().image_settings().file_format().lower()
        file_path = path.join(app_settings().paths().output_dir_path(), file_name)

        # create the output directory if it does not exist
        if not path.exists(app_settings().paths().output_dir_path()):
            makedirs(app_settings().paths().output_dir_path())

        return file_path

    @staticmethod
    def render_file(file_components: list) -> None:
        """ Performs the render for the provided file. """

        file_name = RenderUtility.file_name_for_components(file_components)
        if path.exists(file_name) and not app_settings().parameters().overwrite():
            logger().info("Already exists, skipping: " + file_name)
            return

        time_tracker().start("render")
        # set the file name for the render and render
        context.scene.render.filepath = file_name
        ops.render.render(write_still=True)

        stat_tracker().update_stat("render")
        time_tracker().end("render")
