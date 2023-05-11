""" This utility class contains references to each of the different
    overseer types. It handles the creation and execution of each
    overseer.
"""

from datetime import datetime
from os import path

from src.classes.camera import camera
from src.classes.overseer_dispatcher import overseer_dispatcher
from src.parsers.settings_parser import app_settings, blender_settings
from src.trackers.logger import logger
from src.utilities.material_utility import MaterialUtility
from src.utilities.render_utility import RenderUtility
from src.utilities.validation_utility import ValidationUtility


class OverseerUtility:
    """ This class provides an interface for controlling each of the sub
        overseers easily while performing all of their operations. """

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
        """ Creates the overseer based on the type provided. """

        # executes the generic Overseer dispatcher to the sub overseers
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
        # create the expected overseers
        self.create_overseer('ViewOverseer')
        self.create_overseer('WorldOverseer')
        self.create_overseer('MaterialOverseer',
                             materials=self._materials)

        immaterial_collections = \
            MaterialUtility.get_immaterial_collections()
        # create an overseer for each of the main collections
        for index in reversed(range(len(immaterial_collections))):
            collection = immaterial_collections[index]
            self.create_overseer('CollectionOverseer',
                                 collection=collection,
                                 files=self._files[collection])

    def update(self) -> None:
        """ Updates each of the overseers and executes the rendering. """

        # call into each sub overseer and execute their update
        # on each iteration
        [overseer.update() for overseer in self._overseers]

        # grab the components from the overseers and the settings for the file name
        components = [str(overseer) for overseer in self._overseers]
        components.append(
            blender_settings().image_settings().color_mode().lower()
        )
        components.append(
            blender_settings().image_settings().color_depth()
        )
        # update the camera's perspective and align
        camera().set_camera_to_perspective(
            not app_settings().check_for_orthographic_components(components)
        )
        camera().align_camera_to_active_objects()
        self._count += 1
        filename = path.split(RenderUtility.file_name_for_components(components))[-1]
        logger().info("Render " + str(self._count)
                      + " out of " + str(self.total_iterations_to_execute)
                      + ": " + filename
                      + " @ " + str(datetime.now().strftime("%H:%M:%S")))
        # use the render utility to render the scene
        RenderUtility.render_file(components)
