from os import path

from src.classes.exceptions import InvalidFileException, InvalidMaterialException
from src.classes.world import world
from src.parsers.settings_parser import blender_settings
from src.utilities.append_utility import AppendUtility
from src.utilities.clear_utility import ClearUtility
from src.utilities.clean_utility import CleanUtility
from src.utilities.material_utility import MaterialUtility
from src.utilities.mesh_utility import MeshUtility


class CollectionOverseer:

    def __init__(self,
                 collection: str,
                 files=None,
                 repeat: int = 0) -> None:
        self._collection = collection
        self._files = files
        self._names = CleanUtility.cleanup_file_components(files)
        self._file_index = 0
        self._repeat = max(repeat, 0)
        # force update on first call
        self._current_count = self._repeat

    def update(self) -> None:
        if self._file_index > len(self._files):
            raise InvalidFileException("Hit a file index that is out of the valid range: "
                                       + str(self._file_index) + ", max: "
                                       + str(len(self._files))
                                       + ", for collection: " + self._collection)

        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        ClearUtility.clear_collection(self._collection)
        AppendUtility.append_from_file(self._files[self._file_index], self._collection)
        self._file_index += 1
        self._file_index %= len(self._files)

    def __str__(self):
        # the currently appended file is one before the index tracker
        currently_appended_index = self._file_index - 1
        currently_appended_index %= len(self._files)
        return str(self._names[currently_appended_index])


class MaterialCollectionOverseer:

    def __init__(self,
                 materials: list,
                 repeat: int = 0) -> None:
        self._materials = materials
        self._names = CleanUtility.cleanup_other_components([material.name
                                                             for material in materials])
        self._material_index = 0
        self._repeat = max(repeat, 0)
        self._current_count = self._repeat

    def update(self) -> None:
        if self._material_index > len(self._materials):
            raise InvalidMaterialException("Hit a material index that is out of the valid range: "
                                           + str(self._material_index) + ", max: "
                                           + str(len(self._materials))
                                           + ", for materials")

        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        meshes = MeshUtility.all_meshes_in_scene()
        MaterialUtility.update_meshes_with_material(meshes,
                                                    self._materials[self._material_index])
        self._material_index += 1
        self._material_index %= len(self._materials)

    def __str__(self):
        # the current material is one before the index tracker
        current_material_index = self._material_index - 1
        current_material_index %= len(self._materials)
        return str(self._names[current_material_index])


class WorldOverseer:

    def __init__(self,
                 repeat: int = 0) -> None:
        self._repeat = max(repeat, 0)
        self._current_count = self._repeat
        self._world = world()
        self._current_emission = 0.0
        if blender_settings().background_settings().hdri_enabled():
            world().set_hdri()

    def update(self) -> None:
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        background_settings = blender_settings().background_settings()

        if not background_settings.hdri_enabled():
            emission_value = background_settings.default_emission()

            if background_settings.emission_variability_enabled():
                self._current_emission += background_settings.emission_step()
                if self._current_emission > background_settings.max_emission():
                    self._current_emission = background_settings.emission_step()

                emission_value = self._current_emission

            self._current_count = 0
            world().set_background_emission(emission_value)

    @staticmethod
    def iteration_count() -> int:
        background_settings = blender_settings().background_settings()
        if background_settings.emission_variability_enabled() \
                and not background_settings.hdri_enabled():
            return max(int(background_settings.max_emission()
                           / background_settings.emission_step()), 1)

        return 1

    def __str__(self):
        background_settings = blender_settings().background_settings()
        world_str = ''
        if background_settings.hdri_enabled():
            world_str += path.split(background_settings.hdri())[-1]
        elif background_settings.emission_variability_enabled():
            world_str += 'em' + str(self._current_emission)
        else:
            world_str += 'em' + str(blender_settings().
                                    background_settings().default_emission())

        return world_str
