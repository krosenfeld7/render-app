""" This module handles the core app and exits Blender on completion.
"""

from sys import argv, exit


from src.classes.camera import camera
from src.parsers.directory_parser import parse_directories
from src.parsers.settings_parser import app_settings, blender_settings, type_settings
from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker
from src.utilities.clear_utility import ClearUtility
from src.utilities.material_utility import MaterialUtility
from src.utilities.overseer_utility import OverseerUtility
from src.utilities.settings_utility import SettingsUtility


class Driver:
    """ This class performs the core app code and loop. """

    @staticmethod
    def process(files: dict) -> None:
        """ Handles each of the files provided. This function
            calls into the overseers and executes the main loop. """

        # pass the files and material information to the utility
        # this performs all parsing necessary to determine what will be rendered
        overseer = OverseerUtility(files, MaterialUtility.get_materials(files))

        # we want to indicate if nothing is available to render
        if overseer.total_iterations_to_execute == 0:
            logger().info("No valid renders found")

        # call the overseer update which will dispatch to each of the sub overseers
        for index in range(overseer.total_iterations_to_execute):
            overseer.update()

    @staticmethod
    def driver() -> None:
        """ Core app function that handles set up and calls process(). """

        logger().info(" >>>>>>>>>>>>> Driver Running <<<<<<<<<<<<<")
        # this tracks total time of execution
        time_tracker().start("execution")
        # start by clearing everything from the scene
        ClearUtility.clear_all()
        # realign the camera
        camera().point_camera_at_origin()
        # perform all settings updates
        SettingsUtility.update_settings()
        # parse the each of the directories and pass to the handler function
        Driver.process(parse_directories())

        # perform cleanup, end timers and report all info
        ClearUtility.clear_all()
        time_tracker().end("execution")
        stat_tracker().report_stats()
        time_tracker().report_times()
        logger().info(" >>>>>>>>>>>>> Driver Complete <<<<<<<<<<<<<")


if __name__ == "__main__":
    """ Entry point into the core app. Calls into the
        settings parsers and executes the core function. """
    settings_paths = argv[argv.index("--") + 1:]
    app_settings(settings_paths[0])
    blender_settings(settings_paths[1])
    type_settings(settings_paths[2])
    # settings are parsed, execute core function
    Driver.driver()
    # call exit to kill Blender process
    exit()
