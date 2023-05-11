""" This module provides the in app settings types that store
    the configuration files settings.
"""

from os import path, getcwd
from typing import Optional


class AppSettings:
    """ This class is used to hold the app settings
        specified in app_settings.json. """

    def __init__(self,
                 collections: dict,
                 parameters: dict,
                 paths: dict,
                 constants: Optional[list] = None,
                 material_collection: str = '',
                 blacklist: Optional[list] = None,
                 whitelist: Optional[list] = None,
                 orthographic_components: Optional[list] = None,
                 material_combinations: Optional[list] = None) -> None:
        self._constants = constants
        self._collections = collections
        self._material_collection = material_collection
        self._parameters = AppSettings.Parameters(**parameters)
        self._paths = AppSettings.Paths(**paths)
        self._blacklist = blacklist
        self._whitelist = whitelist
        self._orthographic_components = orthographic_components
        self._material_combinations = material_combinations

    def collections(self) -> dict:
        """ Returns the collections specified in app settings. """

        return self._collections

    def constants(self) -> Optional[list]:
        """ Returns the constants specified in app settings
            if applicable. """

        return self._constants

    def material_collection(self) -> str:
        """ Returns the material collection specified in
            app settings. """

        return self._material_collection

    def parameters(self) -> 'AppSettings.Parameters':
        """ Returns the parameters specified in app settings. """

        return self._parameters

    def paths(self) -> 'AppSettings.Paths':
        """ Returns the paths specified in app settings. """

        return self._paths

    def blacklist(self) -> Optional[list]:
        """ Returns the blacklist specified in app settings
            if applicable. """

        return self._blacklist

    def whitelist(self) -> Optional[list]:
        """ Returns the whitelist specified in app settings
            if applicable. """

        return self._whitelist

    def check_for_orthographic_components(self, components: list) -> bool:
        """ Returns true if any component specified is within the
            orthographic_components field in app settings. """

        if self._orthographic_components is None:
            return False

        return any(component in components
                   for component in self._orthographic_components)

    def orthographic_components(self) -> Optional[list]:
        """ Returns the orthographic components specified in
            app settings. """

        return self._orthographic_components

    def validate_against_blacklist(self,
                                   entry: str) -> bool:
        """ Checks if the entry is not in the blacklist if the
            blacklist is enabled. """

        return self._blacklist is not None and entry \
            not in self._blacklist

    def validate_against_whitelist(self,
                                   entry: str) -> bool:
        """ Checks if the entry is in the whitelist if the
            whitelist is enabled. """

        return self._whitelist is not None and entry in self._whitelist

    def validate_entry(self,
                       entry: str,
                       collection='None') -> bool:
        """ Checks if the entry passes the blacklist/whitelist. """

        if self._parameters.blacklist_enabled():
            return self.validate_against_blacklist(entry)
        elif self._parameters.whitelist_enabled():
            # wildcard selection
            if 'all_' + collection.lower() in self._whitelist:
                return True

            return self.validate_against_whitelist(entry)

        return True

    def material_combinations(self) -> Optional[list]:
        """ Returns the material combinations specified in the
            app settings. """

        return self._material_combinations

    class Paths:
        """ This class is used to hold the path settings
            specified in app_settings.json. """

        def __init__(self,
                     blender_collection_path: str,
                     blender_exe: str,
                     blender_file_extension: str,
                     driver: str,
                     log_dir: str,
                     main_file: str,
                     output_dir: str,
                     search_dir: str) -> None:
            self._blender_collection = blender_collection_path
            self._blender_exe = blender_exe
            self._blender_file_extension = blender_file_extension
            self._driver = driver
            self._log_dir = log_dir
            self._output_dir = output_dir
            self._main_file = main_file
            self._search_dir = search_dir

        def blender_collection(self) -> str:
            """ Returns the blender collection path specified in the
                app settings. """

            return self._blender_collection

        def blender_exe(self) -> str:
            """ Returns the blender exe path specified in the
                app settings. """

            return self._blender_exe

        def blender_file_extension(self) -> str:
            """ Returns the blender file extension specified in the
                app settings. """

            return self._blender_file_extension

        def driver(self) -> str:
            """ Returns the driver script path specified in the
                app settings. """

            return self._driver

        def log_dir(self) -> str:
            """ Returns the log path specified in the app settings. """

            return self._log_dir

        def main_file(self) -> str:
            """ Returns the template blend file path specified in the
                app settings. """

            return self._main_file

        def output_dir_name(self) -> str:
            """ Returns the output directory name specified in the
                app settings. """

            return self._output_dir

        def output_dir_path(self) -> str:
            """ Returns the output directory path specified in the
                app settings. """

            return path.join(getcwd(), self._output_dir)

        def search_dir(self) -> str:
            """ Returns the search directory name specified in the
                app settings. """

            return self._search_dir

        def search_dir_path(self) -> str:
            """ Returns the search directory path specified in the
                app settings. """

            return path.join(getcwd(), self._search_dir)

    class Parameters:
        """ This class is used to hold the parameter settings
            specified in app_settings.json. """

        def __init__(self,
                     enable_blacklist=False,
                     enable_whitelist=False,
                     enable_logging=False,
                     enable_stat_tracking=False,
                     enable_time_tracking=False,
                     overwrite_all=False,
                     enable_material_combinations=False,
                     combinatorial_type='product') -> None:
            self._enable_blacklist = enable_blacklist
            self._enable_whitelist = enable_whitelist
            self._enable_logging = enable_logging
            self._enable_stat_tracking = enable_stat_tracking
            self._enable_time_tracking = enable_time_tracking
            self._overwrite_all = overwrite_all
            self._enable_material_combinations = \
                enable_material_combinations
            self._combinatorial_type = combinatorial_type

        def blacklist_enabled(self) -> bool:
            """ Returns whether the blacklist is enabled in
                app settings parameters. """

            return self._enable_blacklist

        def whitelist_enabled(self) -> bool:
            """ Returns whether whitelist is enabled in
                app settings parameters. """

            return self._enable_whitelist

        def logging_enabled(self) -> bool:
            """ Returns whether logging is enabled in
                app settings parameters. """

            return self._enable_logging

        def overwrite(self) -> bool:
            """ Returns whether overwriting output is enabled in
                app settings parameters. """

            return self._overwrite_all

        def stat_tracking_enabled(self) -> bool:
            """ Returns whether stat tracking is enabled in
                app settings parameters. """

            return self._enable_stat_tracking

        def time_tracking_enabled(self) -> bool:
            """ Returns whether time tracking is enabled in
                app settings parameters. """

            return self._enable_time_tracking

        def enable_material_combinations(self) -> bool:
            """ Returns whether material combinations is enabled in
                app settings parameters. """

            return self._enable_material_combinations

        def combinatorial_type(self) -> str:
            """ Returns the material combination function specified in
                app settings parameters. """

            return self._combinatorial_type


class BlenderSettings:
    """ This class is used to hold the blender settings
        specified in blender_settings.json. """

    def __init__(self,
                 render_settings: dict,
                 eevee_settings: dict,
                 cycles_settings: dict,
                 scene_settings: dict,
                 view_settings: dict,
                 image_settings: dict,
                 background_settings: dict) -> None:
        self._render_settings = \
            BlenderSettings.RenderSettings(**render_settings)
        self._eevee_settings = \
            BlenderSettings.EeveeEngineSettings(**eevee_settings)
        self._cycles_settings = \
            BlenderSettings.CyclesEngineSettings(**cycles_settings)
        self._scene_settings = \
            BlenderSettings.SceneSettings(**scene_settings)
        self._view_settings = \
            BlenderSettings.ViewSettings(**view_settings)
        self._image_settings = \
            BlenderSettings.ImageSettings(**image_settings)
        self._background_settings = \
            BlenderSettings.BackgroundSettings(**background_settings)

    def render_settings(self) -> 'BlenderSettings.RenderSettings':
        """ Returns the render settings specified in the
            blender settings. """

        return self._render_settings

    def eevee_settings(self) -> 'BlenderSettings.EeveeEngineSettings':
        """ Returns the Eevee settings specified in the
            blender settings. """

        return self._eevee_settings

    def cycles_settings(self) -> 'BlenderSettings.CyclesEngineSettings':
        """ Returns the Cycles settings specified in the
            blender settings. """

        return self._cycles_settings

    def scene_settings(self) -> 'BlenderSettings.SceneSettings':
        """ Returns the scene settings specified in the
            blender settings. """

        return self._scene_settings

    def view_settings(self) -> 'BlenderSettings.ViewSettings':
        """ Returns the view settings specified in the
            blender settings. """

        return self._view_settings

    def image_settings(self) -> 'BlenderSettings.ImageSettings':
        """ Returns the image settings specified in the
            blender settings. """

        return self._image_settings

    def background_settings(self) -> 'BlenderSettings.BackgroundSettings':
        """ Returns the background settings specified in the
            blender settings. """

        return self._background_settings

    class RenderSettings:
        """ This class is used to hold the render settings
            specified in blender_settings.json. """

        def __init__(self,
                     render_engine: str,
                     resolution_x: float,
                     resolution_y: float,
                     resolution_percentage: float,
                     use_border=False,
                     film_transparent=False) -> None:
            self._engine = render_engine
            self._resolution_x = resolution_x
            self._resolution_y = resolution_y
            self._resolution_percentage = resolution_percentage
            self._use_border = use_border
            self._film_transparent = film_transparent

        def engine(self) -> str:
            """ Returns the render engine specified in
                render settings. """

            return self._engine

        def res_x(self) -> float:
            """ Returns the x resolution specified in
                render settings. """

            return self._resolution_x

        def res_y(self) -> float:
            """ Returns the y resolution specified in
                render settings. """

            return self._resolution_y

        def res_percent(self) -> float:
            """ Returns the resolution percent specified in
                render settings. """

            return self._resolution_percentage

        def bordered(self) -> bool:
            """ Returns whether render border should be used as
                specified in render settings. """

            return self._use_border

        def transparent_background(self) -> bool:
            """ Returns whether film transparency should be used
                as specified in render settings. """

            return self._film_transparent

    class ViewSettings:
        """ This class is used to hold the view settings
            specified in blender_settings.json. """

        def __init__(self,
                     look: str,
                     view_transform: str,
                     default_exposure: float,
                     exposure_step: float,
                     start_exposure: float,
                     end_exposure: float,
                     enable_exposure_variability: bool) -> None:
            self._look = look
            self._view_transform = view_transform
            self._default_exposure = default_exposure
            self._exposure_step = exposure_step
            self._start_exposure = start_exposure
            self._end_exposure = end_exposure
            self._enable_exposure_variable_rendering = \
                enable_exposure_variability

        def look(self) -> str:
            """ Returns the look as specified in
                view settings. """

            return self._look

        def view_transform(self) -> str:
            """ Returns the view transform as specified in
                view settings. """

            return self._view_transform

        def default_exposure(self) -> float:
            """ Returns the default exposure as specified in
                view settings. """

            return self._default_exposure

        def exposure_step(self) -> float:
            """ Returns the exposure step as specified in
                view settings. """

            return self._exposure_step

        def start_exposure(self) -> float:
            """ Returns the start exposure as specified in
                view settings. """

            return self._start_exposure

        def end_exposure(self) -> float:
            """ Returns the end exposure as specified in
                view settings. """

            return self._end_exposure

        def exposure_variability_enabled(self) -> float:
            """ Returns whether exposure variability is enabled
                as specified in view settings. """

            return self._enable_exposure_variable_rendering

    class SceneSettings:
        """ This class is used to hold the scene settings
            specified in blender_settings.json. """

        def __init__(self,
                     frame_start: int,
                     frame_end: int):
            self._frame_start = frame_start
            self._frame_end = frame_end

        def frame_start(self) -> int:
            """ Returns the start frame as specified in
                scene settings. """

            return self._frame_start

        def frame_end(self) -> int:
            """ Returns the end frame as specified in
                scene settings. """

            return self._frame_end

    class ImageSettings:
        """ This class is used to hold the image settings
            specified in blender_settings.json. """

        def __init__(self,
                     file_format: str,
                     color_mode: str,
                     color_depth: str,
                     compression: int):
            self._file_format = file_format
            self._color_mode = color_mode
            self._color_depth = color_depth
            self._compression = compression

        def file_format(self) -> str:
            """ Returns the file format as specified in
                image settings. """

            return self._file_format

        def color_mode(self) -> str:
            """ Returns the color mode as specified in
                image settings. """

            return self._color_mode

        def color_depth(self) -> str:
            """ Returns the color bit depth as specified in
                image settings. """

            return self._color_depth

        def compression(self) -> int:
            """ Returns the compression amount as specified in
                image settings. """

            return self._compression

    class EeveeEngineSettings:
        """ This class is used to hold the Eevee settings
            specified in blender_settings.json. """

        def __init__(self,
                     samples: int,
                     bloom=False,
                     ambient_occlusion=False,
                     bloom_intensity=0.05) -> None:
            self._taa_render_samples = samples
            self._use_bloom = bloom
            self._use_gtao = ambient_occlusion
            self._bloom_intensity = bloom_intensity

        def samples(self) -> int:
            """ Returns the number of samples as specified in
                Eevee settings. """

            return self._taa_render_samples

        def bloom_enabled(self) -> bool:
            """ Returns whether bloom is enabled as specified in
                Eevee settings. """

            return self._use_bloom

        def ambient_occlusion_enabled(self) -> bool:
            """ Returns whether ambient occlusion is enabled
                as specified in Eevee settings. """

            return self._use_gtao

        def bloom_intensity(self) -> float:
            """ Returns the bloom intensity as specified in
                Eevee settings. """

            return self._bloom_intensity

    class CyclesEngineSettings:
        """ This class is used to hold the Cycles settings
            specified in blender_settings.json. """

        def __init__(self,
                     samples: int,
                     device='CPU') -> None:
            self._samples = samples
            self._device = device

        def samples(self) -> int:
            """ Returns the number of samples as specified in
                Cycles settings. """

            return self._samples

        def device(self) -> str:
            """ Returns the device as specified in
                Cycles settings. """

            return self._device

    class BackgroundSettings:
        """ This class is used to hold the background settings
            specified in blender_settings.json. """

        def __init__(self,
                     emission_color: list,
                     default_emission: float = 0.0,
                     emission_step: float = 0.0,
                     max_emission: float = 0.0,
                     enable_emission_variability=False,
                     enable_hdri=False,
                     hdri_dir='',
                     hdris: list = None) -> None:
            self._default_emission = default_emission
            self._emission_step = emission_step
            self._max_emission = max_emission
            self._emission_color = emission_color
            self._enable_emission_variable_rendering = \
                enable_emission_variability
            self._use_hdri = enable_hdri
            self._hdri_dir = hdri_dir
            self._hdris = hdris

        def default_emission(self) -> float:
            """ Returns the default emission as specified in
                background settings. """

            return self._default_emission

        def emission_step(self) -> float:
            """ Returns the emission step as specified in
                background settings. """

            return self._emission_step

        def max_emission(self) -> float:
            """ Returns the max emission as specified in
                background settings. """

            return self._max_emission

        def emission_color(self) -> list:
            """ Returns the emission color as specified in
                background settings. """

            return self._emission_color

        def emission_variability_enabled(self) -> bool:
            """ Returns whether emission variability is enabled
                as specified in background settings. """

            return self._enable_emission_variable_rendering

        def hdri_enabled(self) -> bool:
            """ Returns whether hdris are enabled as specified in
                background settings. """

            return self._use_hdri

        def hdri_dir(self) -> str:
            """ Returns the hdri search directory as specified in
                background settings. """

            return self._hdri_dir

        def hdris(self) -> list:
            """ Returns the paths to all of the hdris
                as specified in background settings. """

            hdri_paths = list()
            for hdri in self._hdris:
                hdri_path = path.join(getcwd(), self._hdri_dir)
                hdri_paths.append(path.join(hdri_path, hdri))

            return hdri_paths


class TypeSettings:
    """ This class is used to hold the type settings
        specified in type_settings.json. """

    def __init__(self,
                 stat_types: list,
                 time_types: list) -> None:
        self._stat_types = stat_types
        self._time_types = time_types

    def stat_types(self) -> list:
        """ Returns all of the stat types specified in
            type settings. """

        return self._stat_types

    def time_types(self) -> list:
        """ Returns all of the time types specified in
            type settings. """

        return self._time_types
