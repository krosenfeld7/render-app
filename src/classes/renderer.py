from os import path, makedirs
from bpy import context, ops

from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker


class Renderer:

    @staticmethod
    def cleanup_file_components(file_components: list) -> list:
        cleaned_components = list()
        for component in file_components:
            cleaned_component = path.splitext(path.basename(component))[0]
            cleaned_component = ''.join(filter(str.isalnum, cleaned_component)).lower()
            cleaned_components.append(cleaned_component)

        return cleaned_components

    @staticmethod
    def cleanup_info_components(info_components: list) -> list:
        cleaned_components = list()
        for component in info_components:
            cleaned_component = component.replace(" ", "").lower()
            cleaned_components.append(cleaned_component)

        return cleaned_components

    @staticmethod
    def render_file_name(file_components: list, info_components: list) -> str:
        file_components = Renderer.cleanup_file_components(file_components)
        info_components = Renderer.cleanup_info_components(info_components)

        file_name = '_'.join([*file_components, *info_components])
        file_name += '.' + blender_settings().image_settings().file_format().lower()
        file_path = path.join(app_settings().paths().output_dir_path(), file_name)

        if not path.exists(app_settings().paths().output_dir_path()):
            makedirs(app_settings().paths().output_dir_path())

        return file_path

    @staticmethod
    def render_file(file_components: list, info_components: list) -> None:
        time_tracker().start("render")
        logger().info("render_file - started: " + str(file_components))

        output_file = Renderer.render_file_name(file_components, info_components)

        if path.exists(output_file) and not app_settings().parameters().overwrite():
            logger().info("Already exists, skipping: " + output_file)
            return

        context.scene.render.filepath = output_file
        ops.render.render(write_still=True)

        stat_tracker().update_stat("render")
        time_tracker().end("render")

        logger().info("render_file - finished")
