""" This utility class performs updates of settings based on the
    values specified in the configuration files.
"""

from bpy import context
from typing import Any

from src.parsers.settings_parser import blender_settings


class SettingsUtility:
    """ This class provides a number of settings update operations. """

    @staticmethod
    def update_settings() -> None:
        """ Updates all settings. """

        scene = context.scene
        SettingsUtility.update_render_settings(scene)
        SettingsUtility.update_scene_settings(scene)
        SettingsUtility.update_view_settings(scene)
        SettingsUtility.update_image_settings(scene)
        SettingsUtility.update_eevee_settings(scene)
        SettingsUtility.update_cycles_settings(scene)

    @staticmethod
    def update_render_settings(scene: Any) -> None:
        """ Updates render settings. """

        render_settings = blender_settings().render_settings()
        scene.render.engine = render_settings.engine()
        scene.render.resolution_x = render_settings.res_x()
        scene.render.resolution_y = render_settings.res_y()
        scene.render.resolution_percentage = \
            render_settings.res_percent()
        scene.render.use_border = render_settings.bordered()
        scene.render.film_transparent = \
            render_settings.transparent_background()

    @staticmethod
    def update_view_settings(scene: Any) -> None:
        """ Updates view settings. """

        view_settings = blender_settings().view_settings()
        scene.view_settings.look = view_settings.look()
        scene.view_settings.view_transform = view_settings.view_transform()
        scene.view_settings.exposure = view_settings.default_exposure()

    @staticmethod
    def update_scene_settings(scene: Any) -> None:
        """ Updates scene settings. """

        scene_settings = blender_settings().scene_settings()
        scene.frame_start = scene_settings.frame_start()
        scene.frame_end = scene_settings.frame_end()

    @staticmethod
    def update_image_settings(scene: Any) -> None:
        """ Updates image settings. """

        image_settings = blender_settings().image_settings()
        scene.render.image_settings.file_format = image_settings.file_format()
        scene.render.image_settings.color_mode = image_settings.color_mode()
        scene.render.image_settings.color_depth = image_settings.color_depth()
        scene.render.image_settings.compression = image_settings.compression()

    @staticmethod
    def update_eevee_settings(scene: Any) -> None:
        """ Updates Eevee settings. """

        eevee_settings = blender_settings().eevee_settings()
        scene.eevee.taa_render_samples = eevee_settings.samples()
        scene.eevee.use_bloom = eevee_settings.bloom_enabled()
        scene.eevee.use_gtao = eevee_settings.ambient_occlusion_enabled()
        scene.eevee.bloom_intensity = eevee_settings.bloom_intensity()

    @staticmethod
    def update_cycles_settings(scene: Any) -> None:
        """ Updates cycles settings. """

        cycles_settings = blender_settings().cycles_settings()
        scene.cycles.samples = cycles_settings.samples()
        scene.cycles.device = cycles_settings.device()
