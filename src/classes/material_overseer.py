from itertools import combinations, permutations, product

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

    @staticmethod
    def specified_combos(combos: list,
                         combo_length: int) -> list:
        # length is assumed to be correct
        return combos

    func_map = {
        'product': product,
        'combinations': combinations,
        'permutations': permutations,
        'specified': specified_combos
    }

    def __init__(self,
                 repeat: int,
                 materials: list) -> None:
        super(VariableMaterialOverseer, self).__init__(repeat, materials)
        self._materials_by_names = dict()
        for index in range(len(self._materials)):
            self._materials_by_names[self._names[index]] = self._materials[index]

        self._immaterial_collections = MaterialUtility.get_immaterial_collections()
        function = self.func_map[app_settings().parameters().combinatorial_type()]
        self._material_combinations = list(function(app_settings().material_combinations(),
                                                    len(self._immaterial_collections)))
        self._material_combo_index = 0

    def update(self) -> None:
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0

        material_combo = self._material_combinations[self._material_combo_index]
        for index in range(len(self._immaterial_collections)):
            collection = self._immaterial_collections[index]
            material_name = material_combo[index]

            meshes = MeshUtility.all_meshes_in_collection(collection)
            if material_name not in self._materials_by_names:
                raise InvalidConfigurationException("Material: " + material_name + " not specified")

            MaterialUtility.update_meshes_with_material(meshes,
                                                        self._materials_by_names[material_name])

        self._material_combo_index += 1
        self._material_combo_index %= len(self._material_combinations)

    def iteration_count(self) -> int:
        return len(self._material_combinations)

    def __str__(self):
        current_index = self._material_combo_index - 1
        current_index %= len(self._material_combinations)
        accounted = set()
        duplicates_removed = [component
                              for component in self._material_combinations[current_index]
                              if not (component in accounted or accounted.add(component))]
        return '_'.join(duplicates_removed)


def material_dispatcher(*args, **kwargs) -> MaterialOverseer:
    if app_settings().parameters().enable_material_combinations() \
            and app_settings().material_combinations() is not None:
        return VariableMaterialOverseer(*args, **kwargs)

    return DefaultMaterialOverseer(*args, **kwargs)
