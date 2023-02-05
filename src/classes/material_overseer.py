
from src.classes.exceptions import InvalidConfigurationException, InvalidMaterialException
from src.classes.overseer import Overseer
from src.parsers.settings_parser import app_settings
from src.utilities.clean_utility import CleanUtility
from src.utilities.material_utility import MaterialUtility
from src.utilities.mesh_utility import MeshUtility


class MaterialOverseer(Overseer):

    def __init__(self,
                 repeat: int,
                 materials: list) -> None:
        super(MaterialOverseer, self).__init__(repeat)
        self._materials = materials
        self._names = CleanUtility.cleanup_other_components([material.name
                                                             for material in materials])
        self._material_index = 0

    def update(self) -> None:
        raise NotImplementedError("MaterialOverseer update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("MaterialOverseer iteration_count must be implemented")


class DefaultMaterialOverseer(MaterialOverseer):

    def __init__(self,
                 repeat: int,
                 materials: list) -> None:
        super(DefaultMaterialOverseer, self).__init__(repeat, materials)

    def update(self) -> None:
        if self._material_index >= len(self._materials):
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

    def iteration_count(self) -> int:
        return len(self._materials)

    def __str__(self):
        # the current material is one before the index tracker
        current_material_index = self._material_index - 1
        current_material_index %= len(self._materials)
        return str(self._names[current_material_index])


class VariableMaterialOverseer(MaterialOverseer):

    def __init__(self,
                 repeat: int,
                 materials: list) -> None:
        super(VariableMaterialOverseer, self).__init__(repeat, materials)
        self._materials_by_names = dict()
        for index in range(len(self._materials)):
            self._materials_by_names[self._names[index]] = self._materials[index]

        self._material_name_by_collection = app_settings().material_to_collection()

    def update(self) -> None:
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        for collection in self._material_name_by_collection:
            meshes = MeshUtility.all_meshes_in_collection(collection)
            material_name = self._material_name_by_collection[collection]
            if material_name not in self._materials_by_names:
                raise InvalidConfigurationException("Material: " + material_name + " not specified")

            MaterialUtility.update_meshes_with_material(meshes,
                                                        self._materials_by_names[material_name])

    def iteration_count(self) -> int:
        return 1

    def __str__(self):
        return '_'.join(list(self._material_name_by_collection.values()))


def material_dispatcher(*args, **kwargs) -> MaterialOverseer:
    if app_settings().parameters().material_to_collection_enabled():
        return VariableMaterialOverseer(*args, **kwargs)

    return DefaultMaterialOverseer(*args, **kwargs)
