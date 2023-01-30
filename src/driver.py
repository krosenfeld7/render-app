from sys import argv, exit


from src.classes.camera import camera
from src.utilities.render_utility import RenderUtility
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

    @staticmethod
    def process(files: dict) -> None:
        overseer = OverseerUtility(files, MaterialUtility.get_materials(files))

        for index in range(overseer.total_iterations_to_execute):
            RenderUtility.render_file(overseer.update())

    @staticmethod
    def driver() -> None:
        logger().info(" >>>>>>>>>>>>> Driver Running  <<<<<<<<<<<<<")
        time_tracker().start("execution")

        ClearUtility.clear_all()
        camera().point_camera_at_origin()
        SettingsUtility.update_settings()
        Driver.process(parse_directories())

        ClearUtility.clear_all()
        time_tracker().end("execution")
        stat_tracker().report_stats()
        time_tracker().report_times()
        logger().info(" >>>>>>>>>>>>> Driver Complete <<<<<<<<<<<<<")


if __name__ == "__main__":
    settings_paths = argv[argv.index("--") + 1:]
    app_settings(settings_paths[0])
    blender_settings(settings_paths[1])
    type_settings(settings_paths[2])
    Driver.driver()

    exit()
