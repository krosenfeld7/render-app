""" This module provides time tracking to the app.
"""

from time import time
from typing import Optional

from src.classes.exceptions import TimeTypeNotFoundException
from src.parsers.settings_parser import app_settings, type_settings
from src.trackers.logger import logger


class TimeTracker:
    """ This class provides a straightforward way to perform time
        tracking across all of the types specified in the configuration
        files. """

    class TimeReport:
        """ This class is used to hold the data for a time report. These
            reports are then aggregated to provide the all the times for
            the app run. """

        def __init__(self,
                     time_type: str,
                     elapsed: float,
                     collection: Optional[str] = None) -> None:
            self._time_type = time_type
            self._collection = collection
            self._elapsed = elapsed

        def get_time_type(self) -> str:
            """ Returns this time report's type. """

            return self._time_type

        def get_collection(self) -> Optional[str]:
            """ Returns this time report's collection if applicable. """

            return self._collection

        def get_elapsed(self) -> float:
            """ Returns this time report's time value. """

            return self._elapsed

        def set_elapsed(self,
                        elapsed: float) -> None:
            """ Updates this time report's time value. """

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
        """ Starts the timer for this time type and collection. """

        if not app_settings().parameters().time_tracking_enabled():
            return

        if time_type not in self._time_types:
            raise TimeTypeNotFoundException("Invalid time type: "
                                            + time_type)

        # Add the time object to the active times for tracking purposes.
        # This retains references to the active objects and will be removed
        # upon execution of end.
        self._active_times[(time_type, collection)] = \
            TimeTracker.TimeReport(time_type, time(), collection)

    def end(self,
            time_type: str,
            collection: Optional[str] = None) -> None:
        """ Ends the timer for this time type and collection. """

        if not app_settings().parameters().time_tracking_enabled():
            return

        if time_type not in self._time_types:
            raise TimeTypeNotFoundException("Invalid time type: "
                                            + time_type)

        # Report the invalid call to end().
        if (time_type, collection) not in self._active_times:
            logger().error("TimeTracker::end() - time_type: " + time_type
                           + ", collection: " + str(collection)
                           + " - report not found in time tracker")
            return

        # Remove the report from the active list and report
        # with the elapsed time
        report = self._active_times.pop((time_type, collection))
        report.set_elapsed(time() - report.get_elapsed())
        self._time_report.append(report)

    def _aggregate_by_type(self,
                           time_type: str) -> list:
        """ Helper function that returns all of the reports for the provided
            time type. """

        if time_type not in self._time_types:
            raise TimeTypeNotFoundException("Invalid time type: " + time_type)

        return [report for report in self._time_report
                if report.get_time_type() == time_type]

    def report_times(self) -> None:
        """ Reports all of the tracked times. """

        if not app_settings().parameters().time_tracking_enabled():
            return

        # sum all execution report elapsed times
        total_exec_time = sum(
            [report.get_elapsed() for report in self._time_report
             if report.get_time_type() == 'execution'])

        logger().info("------------- Execution Times -------------")
        logger().info("Type, % of Total, Total Time")
        for time_type in self._time_types:
            # sums the elapsed times of all reports with this type
            total_time_by_type = sum([report.get_elapsed()
                                     for report in self._aggregate_by_type(time_type)])
            pct_total_time = total_time_by_type/total_exec_time * 100
            logger().info(time_type
                          + str(", {0:.2f}%".format(pct_total_time))
                          + ", " + str(total_time_by_type))


_instance = None


def time_tracker() -> TimeTracker:
    """ Singleton accessor for this class. """

    global _instance
    if _instance is None:
        _instance = TimeTracker(type_settings().time_types(),
                                list(app_settings().collections().values()))

    return _instance
