from sys import argv, exit
from itertools import combinations
from bpy import data, ops

from src.classes.camera import camera
from src.classes.collection_overseer import CollectionOverseer, MaterialCollectionOverseer, WorldOverseer
from src.classes.renderer import Renderer
from src.classes.world import world
from src.parsers.directory_parser import parse_directories
from src.parsers.settings_parser import app_settings, blender_settings, type_settings
from src.trackers.logger import logger
from src.trackers.stat_tracker import stat_tracker
from src.trackers.time_tracker import time_tracker
from src.utilities.append_utility import AppendUtility
from src.utilities.clear_utility import ClearUtility
from src.utilities.driver_utility import DriverUtility
from src.utilities.material_utility import MaterialUtility
from src.utilities.mesh_utility import MeshUtility
from src.utilities.settings_utility import SettingsUtility


class Driver:

    @staticmethod
    def process(files: dict) -> None:
        materials_collections = list()
        for materials_dir in app_settings().material_collections():
            for file in files[materials_dir]:
                for collection in app_settings().material_collections():
                    AppendUtility.append_from_file(file, collection)
                    materials_collections.append(collection)

        materials = MaterialUtility.get_materials(materials_collections)

        keys = sorted(app_settings().collections().keys())
        visible_collections_by_priority = list()
        for key in keys:
            if app_settings().collections()[key] not in app_settings().material_collections():
                visible_collections_by_priority.append(app_settings().collections()[key])

        loop_iterations = 0
        world_overseer = WorldOverseer(loop_iterations)
        loop_iterations = WorldOverseer.emissions_count()
        material_collection_overseer = MaterialCollectionOverseer(materials, loop_iterations - 1)

        loop_iterations *= len(materials)

        overseers = list()
        for index in reversed(range(len(visible_collections_by_priority))):
            collection = visible_collections_by_priority[index]
            overseer = CollectionOverseer(collection, files[collection], loop_iterations)
            overseers.insert(0, overseer)

            loop_iterations *= len(files[collection])

        overseers.append(material_collection_overseer)
        overseers.append(world_overseer)

        for index in range(20):
            [overseer.update() for overseer in overseers]
            camera().align_camera_to_active_objects()

            file_components = [str(overseer) for overseer in overseers if isinstance(overseer, CollectionOverseer)]
            info_components = [str(overseer) for overseer in overseers if not isinstance(overseer, CollectionOverseer)]
            Renderer.render_file(file_components, info_components)

    @staticmethod
    def validate_settings() -> None:
        if app_settings().parameters().blacklist_enabled():
            logger().info("Using blacklist: " + str(app_settings().blacklist()))
            if app_settings().blacklist() is None:
                logger().info("Blacklist is empty!")
        if app_settings().parameters().whitelist_enabled():
            logger().info("Using whitelist: " + str(app_settings().whitelist()))
            if app_settings().whitelist() is None:
                logger().info("Whitelist is empty!")

    @staticmethod
    def driver() -> None:
        logger().info(" >>>>>>>>>>>>> Driver Running  <<<<<<<<<<<<<")
        time_tracker().start("execution")

        Driver.validate_settings()
        ClearUtility.clear_all()
        camera().point_camera_at_origin()
        SettingsUtility.update_settings()

        files_by_directory = parse_directories()
        Driver.process(files_by_directory)

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
