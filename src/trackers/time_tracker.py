from time import time
from typing import Optional

from src.classes.exceptions import TimeTypeNotFoundException, \
                                   CollectionNotFoundException
from src.parsers.settings_parser import app_settings, type_settings
from src.trackers.logger import logger


class TimeTracker:

    class TimeReport:
        def __init__(self,
                     time_type: str,
                     elapsed: float,
                     collection: Optional[str] = None) -> None:
            self._time_type = time_type
            self._collection = collection
            self._elapsed = elapsed

        def get_time_type(self) -> str:
            return self._time_type

        def get_collection(self) -> Optional[str]:
            return self._collection

        def get_elapsed(self) -> float:
            return self._elapsed

        def set_elapsed(self,
                        elapsed: float) -> None:
            self._elapsed = elapsed

        def __str__(self) -> str:
            return "Time: " + self._time_type \
                   + ", Collection: " + str(self._collection) \
                   + ", Elapsed: " + str(self._elapsed)

    def __init__(self,
                 time_types: list,
                 collections: list) -> None:
        self._time_types = time_types
        self._collections = collections
        self._time_report = list()
        self._active_times = dict()

    def start(self,
              time_type: str,
              collection: Optional[str] = None) -> None:
        if time_type not in self._time_types:
            raise TimeTypeNotFoundException("Invalid time type: " + time_type)

        self._active_times[(time_type, collection)] = \
            TimeTracker.TimeReport(time_type, time(), collection)

    def end(self,
            time_type: str,
            collection: Optional[str] = None) -> None:
        if time_type not in self._time_types:
            raise TimeTypeNotFoundException("Invalid time type: " + time_type)

        if (time_type, collection) not in self._active_times:
            logger().error("TimeTracker::end() - time_type: " + time_type
                           + ", collection: " + str(collection)
                           + " - report not found in time tracker")
            return

        report = self._active_times.pop((time_type, collection))
        report.set_elapsed(time() - report.get_elapsed())
        self._time_report.append(report)

    def _aggregate_by_type(self,
                           time_type: str) -> list:
        if time_type not in self._time_types:
            raise TimeTypeNotFoundException("Invalid time type: " + time_type)

        reports_by_type = list()
        for report in self._time_report:
            if report.get_time_type() == time_type:
                reports_by_type.append(report)

        return reports_by_type

    def report_times(self) -> None:
        if app_settings().parameters().time_tracking_enabled():
            logger().info("------------- Execution Times -------------")
            for time_type in self._time_types:
                total_time_by_type = sum(report.get_elapsed() for report in self._aggregate_by_type(time_type))
                logger().info(time_type + ": " + str(total_time_by_type))


_instance = None


def time_tracker() -> TimeTracker:
    global _instance
    if _instance is None:
        _instance = TimeTracker(type_settings().time_types(),
                                list(app_settings().collections().values()))

    return _instance
