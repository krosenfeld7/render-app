from os import path, getcwd
from typing import Optional


class AppSettings:
    def __init__(self,
                 collections: dict,
                 parameters: dict,
                 paths: dict,
                 constants: Optional[list] = None,
                 material_collection: str = '',
                 blacklist: Optional[list] = None,
                 whitelist: Optional[list] = None,
                 orthographic_components: Optional[list] = None) -> None:
        self._constants = constants
        self._collections = collections
        self._material_collection = material_collection
        self._parameters = AppSettings.Parameters(**parameters)
        self._paths = AppSettings.Paths(**paths)
        self._blacklist = blacklist
        self._whitelist = whitelist
        self._orthographic_components = orthographic_components

    def collections(self) -> dict:
        return self._collections

    def constants(self) -> Optional[list]:
        return self._constants

    def material_collection(self) -> str:
        return self._material_collection

    def parameters(self) -> 'AppSettings.Parameters':
        return self._parameters

    def paths(self) -> 'AppSettings.Paths':
        return self._paths

    def blacklist(self) -> Optional[list]:
        return self._blacklist

    def whitelist(self) -> Optional[list]:
        return self._whitelist

    def check_for_orthographic_components(self, components: list) -> bool:
        return any(component in components
                   for component in self.orthographic_components())

    def orthographic_components(self) -> Optional[list]:
        return self._orthographic_components

    def validate_against_blacklist(self,
                                   entry: str) -> bool:
        return entry not in self._blacklist

    def validate_against_whitelist(self,
                                   entry: str) -> bool:
        return entry in self._whitelist

    def validate_entry(self,
                       entry: str,
                       collection='None') -> bool:
        if self._parameters.blacklist_enabled():
            return self.validate_against_blacklist(entry)
        elif self._parameters.whitelist_enabled():
            if 'all_' + collection.lower() in self._whitelist:
                return True

            return self.validate_against_whitelist(entry)

        return True

    class Paths:
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
            return self._blender_collection

        def blender_exe(self) -> str:
            return self._blender_exe

        def blender_file_extension(self) -> str:
            return self._blender_file_extension

        def driver(self) -> str:
            return self._driver

        def log_dir(self) -> str:
            return self._log_dir

        def main_file(self) -> str:
            return self._main_file

        def output_dir_name(self) -> str:
            return self._output_dir

        def output_dir_path(self) -> str:
            return path.join(getcwd(), self._output_dir)

        def search_dir(self) -> str:
            return self._search_dir

        def search_dir_path(self) -> str:
            return path.join(getcwd(), self._search_dir)

    class Parameters:
        def __init__(self,
                     enable_blacklist=False,
                     enable_whitelist=False,
                     enable_logging=False,
                     enable_stat_tracking=False,
                     enable_time_tracking=False,
                     overwrite_all=False) -> None:
            self._enable_blacklist = enable_blacklist
            self._enable_whitelist = enable_whitelist
            self._enable_logging = enable_logging
            self._enable_stat_tracking = enable_stat_tracking
            self._enable_time_tracking = enable_time_tracking
            self._overwrite_all = overwrite_all

        def blacklist_enabled(self) -> bool:
            return self._enable_blacklist

        def whitelist_enabled(self) -> bool:
            return self._enable_whitelist

        def logging_enabled(self) -> bool:
            return self._enable_logging

        def overwrite(self) -> bool:
            return self._overwrite_all

        def stat_tracking_enabled(self) -> bool:
            return self._enable_stat_tracking

        def time_tracking_enabled(self) -> bool:
            return self._enable_time_tracking


class BlenderSettings:

    def __init__(self,
                 render_settings: dict,
                 eevee_settings: dict,
                 cycles_settings: dict,
                 scene_settings: dict,
                 view_settings: dict,
                 image_settings: dict,
                 background_settings: dict) -> None:
        self._render_settings = BlenderSettings.RenderSettings(**render_settings)
        self._eevee_settings = BlenderSettings.EeveeEngineSettings(**eevee_settings)
        self._cycles_settings = BlenderSettings.CyclesEngineSettings(**cycles_settings)
        self._scene_settings = BlenderSettings.SceneSettings(**scene_settings)
        self._view_settings = BlenderSettings.ViewSettings(**view_settings)
        self._image_settings = BlenderSettings.ImageSettings(**image_settings)
        self._background_settings = BlenderSettings.BackgroundSettings(**background_settings)

    def render_settings(self) -> 'BlenderSettings.RenderSettings':
        return self._render_settings

    def eevee_settings(self) -> 'BlenderSettings.EeveeEngineSettings':
        return self._eevee_settings

    def cycles_settings(self) -> 'BlenderSettings.CyclesEngineSettings':
        return self._cycles_settings

    def scene_settings(self) -> 'BlenderSettings.SceneSettings':
        return self._scene_settings

    def view_settings(self) -> 'BlenderSettings.ViewSettings':
        return self._view_settings

    def image_settings(self) -> 'BlenderSettings.ImageSettings':
        return self._image_settings

    def background_settings(self) -> 'BlenderSettings.BackgroundSettings':
        return self._background_settings

    class RenderSettings:
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
            return self._engine

        def res_x(self) -> float:
            return self._resolution_x

        def res_y(self) -> float:
            return self._resolution_y

        def res_percent(self) -> float:
            return self._resolution_percentage

        def bordered(self) -> bool:
            return self._use_border

        def transparent_background(self) -> bool:
            return self._film_transparent

    class ViewSettings:
        def __init__(self,
                     look: str,
                     view_transform: str,
                     exposure: float) -> None:
            self._look = look
            self._view_transform = view_transform
            self._exposure = exposure

        def look(self) -> str:
            return self._look

        def view_transform(self) -> str:
            return self._view_transform

        def exposure(self) -> float:
            return self._exposure

    class SceneSettings:
        def __init__(self,
                     frame_start: int,
                     frame_end: int):
            self._frame_start = frame_start
            self._frame_end = frame_end

        def frame_start(self) -> int:
            return self._frame_start

        def frame_end(self) -> int:
            return self._frame_end

    class ImageSettings:
        def __init__(self,
                     file_format: str,
                     color_mode: str,
                     color_depth: str):
            self._file_format = file_format
            self._color_mode = color_mode
            self._color_depth = color_depth

        def file_format(self) -> str:
            return self._file_format

        def color_mode(self) -> str:
            return self._color_mode

        def color_depth(self) -> str:
            return self._color_depth

    class EeveeEngineSettings:
        def __init__(self,
                     samples: int,
                     bloom=False,
                     ambient_occlusion=False) -> None:
            self._taa_render_samples = samples
            self._use_bloom = bloom
            self._use_gtao = ambient_occlusion

        def samples(self) -> int:
            return self._taa_render_samples

        def bloom_enabled(self) -> bool:
            return self._use_bloom

        def ambient_occlusion_enabled(self) -> bool:
            return self._use_gtao

    class CyclesEngineSettings:
        def __init__(self,
                     samples: int,
                     device='CPU') -> None:
            self._samples = samples
            self._device = device

        def samples(self) -> int:
            return self._samples

        def device(self) -> str:
            return self._device

    class BackgroundSettings:
        def __init__(self,
                     emission_color: list,
                     default_emission: Optional[float] = None,
                     emission_step: Optional[float] = None,
                     max_emission: Optional[float] = None,
                     enable_emission_variable_rendering=False,
                     use_hdri=False,
                     hdri='') -> None:
            self._default_emission = default_emission
            self._emission_step = emission_step
            self._max_emission = max_emission
            self._emission_color = emission_color
            self._enable_emission_variable_rendering = \
                enable_emission_variable_rendering
            self._use_hdri = use_hdri
            self._hdri = hdri

        def default_emission(self) -> Optional[float]:
            return self._default_emission

        def emission_step(self) -> Optional[float]:
            return self._emission_step

        def max_emission(self) -> Optional[float]:
            return self._max_emission

        def emission_color(self) -> list:
            return self._emission_color

        def emission_variability_enabled(self) -> bool:
            return self._enable_emission_variable_rendering

        def hdri_enabled(self) -> bool:
            return self._use_hdri

        def hdri(self) -> str:
            return self._hdri

        def hdri_path(self) -> str:
            return path.join(getcwd(), self._hdri)


class TypeSettings:

    def __init__(self,
                 stat_types: list,
                 time_types: list,
                 collection_regex: str) -> None:
        self._stat_types = stat_types
        self._time_types = time_types
        self._collection_regex = collection_regex

    def stat_types(self) -> list:
        return self._stat_types

    def time_types(self) -> list:
        return self._time_types

    def collection_regex(self) -> str:
        return self._collection_regex
