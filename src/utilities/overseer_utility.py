from os import path
from datetime import datetime

from src.classes.camera import camera
from src.classes.overseer_dispatcher import overseer_dispatcher
from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.logger import logger
from src.utilities.material_utility import MaterialUtility
from src.utilities.render_utility import RenderUtility
from src.utilities.validation_utility import ValidationUtility


class OverseerUtility:

    def __init__(self, files: dict, materials: list) -> None:
        self._overseers = list()
        self._materials = ValidationUtility.validate_materials(materials)
        self._files = ValidationUtility.validate_files(files)
        self.total_iterations_to_execute = 0
        self.create_overseers()
        self._count = 0

    def create_overseer(self,
                        overseer_type,
                        **kwargs) -> None:
        overseer = overseer_dispatcher(overseer_type,
                                       self.total_iterations_to_execute,
                                       **kwargs)
        self.total_iterations_to_execute *= overseer.iteration_count()
        self._overseers.insert(0, overseer)

    def create_overseers(self) -> None:
        if self._overseers:
            logger().error("Already created the overseers")
            return

        self.total_iterations_to_execute = 1
        self.create_overseer('ViewOverseer')
        self.create_overseer('WorldOverseer')
        self.create_overseer('MaterialOverseer',
                             materials=self._materials)

        immaterial_collections = MaterialUtility.get_immaterial_collections()
        for index in reversed(range(len(immaterial_collections))):
            collection = immaterial_collections[index]
            self.create_overseer('CollectionOverseer',
                                 collection=collection,
                                 files=self._files[collection])

    def update(self) -> None:
        [overseer.update() for overseer in self._overseers]

        components = [str(overseer) for overseer in self._overseers]
        components.append(blender_settings().image_settings().color_mode().lower())
        components.append(blender_settings().image_settings().color_depth())
        camera().set_camera_to_perspective(not app_settings().
                                           check_for_orthographic_components(components))
        camera().align_camera_to_active_objects()
        self._count += 1
        logger().info("Render " + str(self._count)
                      + " out of " + str(self.total_iterations_to_execute)
                      + ": " + path.split(RenderUtility.file_name_for_components(components))[-1]
                      + " @ " + str(datetime.now().strftime("%H:%M:%S")))
        RenderUtility.render_file(components)
