""" This module provides the different overseers for materials.
    This provides a simple interface for selecting the correct type.
"""

from itertools import combinations, permutations, product

from src.classes.exceptions import InvalidConfigurationException, \
    InvalidMaterialException
from src.classes.overseer import Overseer
from src.parsers.settings_parser import app_settings
from src.utilities.clean_utility import CleanUtility
from src.utilities.material_utility import MaterialUtility
from src.utilities.mesh_utility import MeshUtility


class MaterialOverseer(Overseer):
    """ This class provides the generic material overseer class. This is
        intended to be inherited. """

    def __init__(self,
                 repeat: int,
                 materials: list) -> None:
        super(MaterialOverseer, self).__init__(repeat)
        self._materials = materials
        self._names = CleanUtility.cleanup_other_components(
            [material.name for material in materials]
        )
        self._material_index = 0

    def update(self) -> None:
        raise NotImplementedError("MaterialOverseer "
                                  "update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("MaterialOverseer "
                                  "iteration_count must be implemented")


class DefaultMaterialOverseer(MaterialOverseer):
    """ This class provides the default material overseer.
        This supports applying each material to each object in the scene. """

    def __init__(self,
                 repeat: int,
                 materials: list) -> None:
        super(DefaultMaterialOverseer, self).__init__(repeat, materials)

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state.
            This overseer simply sets the all meshes material to the next
            material in order. """

        # ensure that we are using a valid material
        if self._material_index >= len(self._materials):
            raise InvalidMaterialException("Hit a material index that is "
                                           "out of the valid range: "
                                           + str(self._material_index)
                                           + ", max: "
                                           + str(len(self._materials))
                                           + ", for materials")

        # only perform the update when required
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        # set the material of all meshes in the scene
        meshes = MeshUtility.all_meshes_in_scene()
        MaterialUtility.update_meshes_with_material(
            meshes, self._materials[self._material_index]
        )
        self._material_index += 1
        self._material_index %= len(self._materials)

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. This is equivalent
            to the number of materials. """

        return len(self._materials)

    def __str__(self):
        # the current material is one before the index tracker
        current_material_index = self._material_index - 1
        current_material_index %= len(self._materials)
        return str(self._names[current_material_index])


class VariableMaterialOverseer(MaterialOverseer):
    """ This class provides the variable material overseer.
        This supports applying each material to different collections in the
        scene. See README for details about each type. """

    @staticmethod
    def specified_combos(combos: list,
                         combo_length: int) -> list:
        """ Each specified material is applied to the
            collection that aligns with it in priority order"""

        if combo_length < len(app_settings().collections()):
            raise InvalidMaterialException(
                "Insufficient specified materials for material_combinations, "
                "expected: f{len(app_settings().collections())}, "
                "got: f{combo_length}")

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
        # retrieves the material names for each material
        for index in range(len(self._materials)):
            self._materials_by_names[self._names[index]] = \
                self._materials[index]

        # retrieves all collections that are not material collections
        self._immaterial_collections = MaterialUtility.get_immaterial_collections()
        function = self.func_map[app_settings().parameters().combinatorial_type()]
        # compute the material combinations based on the method provided
        self._material_combinations = list(function(
            app_settings().material_combinations(),
            len(self._immaterial_collections)
        ))
        self._material_combo_index = 0

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state.
            This overseer sets the materials of meshes based on the combinations. """

        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0

        material_combo = self._material_combinations[self._material_combo_index]
        for index in range(len(self._immaterial_collections)):
            collection = self._immaterial_collections[index]
            material_name = material_combo[index]

            # updates all meshes in the collection with the correct
            # material as specified for this combination
            meshes = MeshUtility.all_meshes_in_collection(collection)
            if material_name not in self._materials_by_names:
                raise InvalidConfigurationException("Material: "
                                                    + material_name
                                                    + " not specified")

            # perform the update
            MaterialUtility.update_meshes_with_material(
                meshes, self._materials_by_names[material_name]
            )

        self._material_combo_index += 1
        self._material_combo_index %= len(self._material_combinations)

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. This is equivalent
            to the number of material combinations. """

        return len(self._material_combinations)

    def __str__(self):
        current_index = self._material_combo_index - 1
        current_index %= len(self._material_combinations)
        accounted = set()
        # we don't want to output the same material name twice, this handles duplicates
        duplicates_removed = [component
                              for component in self._material_combinations[current_index]
                              if not (component in accounted or accounted.add(component))]
        return '_'.join(duplicates_removed)


def material_dispatcher(*args, **kwargs) -> MaterialOverseer:
    """ Provides dispatch access to each of the MaterialOverseer types based
        upon the settings. """

    if app_settings().parameters().enable_material_combinations() \
            and app_settings().material_combinations() is not None:
        return VariableMaterialOverseer(*args, **kwargs)

    return DefaultMaterialOverseer(*args, **kwargs)
