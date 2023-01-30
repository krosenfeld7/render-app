from src.classes.camera import camera
from src.classes.overseer import CollectionOverseer, MaterialCollectionOverseer, WorldOverseer
from src.parsers.settings_parser import app_settings
from src.trackers.logger import logger
from src.utilities.material_utility import MaterialUtility
from src.utilities.validation_utility import ValidationUtility


class OverseerUtility:

    def __init__(self, files: dict, materials: list) -> None:
        self._overseers = list()
        self._materials = ValidationUtility.validate_materials(materials)
        self._files = ValidationUtility.validate_files(files)
        self.total_iterations_to_execute = 0
        self.create_overseers()

    def create_collection_overseers(self) -> None:
        immaterial_collections = MaterialUtility.get_immaterial_collections()
        for index in reversed(range(len(immaterial_collections))):
            collection = immaterial_collections[index]
            overseer = CollectionOverseer(collection, self._files[collection],
                                          self.total_iterations_to_execute - 1)
            self._overseers.insert(0, overseer)

            self.total_iterations_to_execute *= len(self._files[collection])

    def create_overseers(self) -> None:
        if self._overseers:
            logger().error("Already created the overseers")
            return

        # create the overseers in reverse order so we know how many times everything needs to execute
        self.total_iterations_to_execute = 0
        world_overseer = WorldOverseer(self.total_iterations_to_execute)
        self.total_iterations_to_execute = WorldOverseer.iteration_count()
        material_collection_overseer = MaterialCollectionOverseer(self._materials,
                                                                  self.total_iterations_to_execute - 1)
        self.total_iterations_to_execute *= len(self._materials)
        self.create_collection_overseers()
        self._overseers.append(material_collection_overseer)
        self._overseers.append(world_overseer)

    def update(self) -> list:
        [overseer.update() for overseer in self._overseers]

        components = [str(overseer) for overseer in self._overseers]
        camera().set_camera_to_perspective(not app_settings().
                                           check_for_orthographic_components(components))
        camera().align_camera_to_active_objects()

        return components
