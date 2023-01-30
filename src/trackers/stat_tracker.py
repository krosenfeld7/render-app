from typing import Optional

from src.classes.exceptions import StatTypeNotFoundException
from src.parsers.settings_parser import app_settings, type_settings
from src.trackers.logger import logger


class StatTracker:

    class StatReport:
        def __init__(self,
                     stat_type: str,
                     collection: Optional[str] = None,
                     msg: Optional[str] = None) -> None:
            self._stat = stat_type
            self._collection = collection
            self._msg = msg
            self._count = 1

        def get_stat_type(self) -> str:
            return self._stat

        def get_collection(self) -> Optional[str]:
            return self._collection

        def get_message(self) -> Optional[str]:
            return self._msg

        def count(self) -> int:
            return self._count

        def increase_count(self) -> None:
            self._count += 1

        def __str__(self) -> str:
            stat_str = "Stat: " + self._stat
            if self._collection is not None:
                stat_str += ", Collection: " + str(self._collection)
            if self._msg is not None:
                stat_str += ", Msg: " + str(self._msg)

            stat_str += ", Count: " + str(self._count)
            return stat_str

    def __init__(self,
                 stat_types: list,
                 collections: list) -> None:
        self._stat_types = stat_types
        self._collections = collections
        self._stats_report = dict()

    def update_stat(self,
                    stat_type: str,
                    collection: Optional[str] = None,
                    msg: Optional[str] = None) -> None:
        if stat_type not in self._stat_types:
            raise StatTypeNotFoundException("Invalid stat type: " + str(stat_type))

        stat_key = (stat_type, collection)
        if stat_key not in self._stats_report:
            self._stats_report[stat_key] = \
                StatTracker.StatReport(stat_type, collection, msg)
        else:
            self._stats_report[stat_key].increase_count()

    def report_stats(self) -> None:
        if app_settings().parameters().stat_tracking_enabled():
            logger().info("------------- Execution Stats -------------")
            for stat in self._stats_report:
                logger().info(str(self._stats_report[stat]))


_instance = None


def stat_tracker() -> StatTracker:
    global _instance
    if _instance is None:
        _instance = StatTracker(type_settings().stat_types(),
                                list(app_settings().collections().values()))

    return _instance
