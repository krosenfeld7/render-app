""" This module contains the generic Overseer type.
    This is intended to be inherited.
"""


class Overseer:
    """ This class provides the default overseer. This is intended to be
        inherited. """

    def __init__(self,
                 repeat: int) -> None:
        """ Repeat allows for inherited classes to ignore the update call
            until the repeat count is met. """

        self._repeat = max(repeat - 1, 0)
        self._current_count = self._repeat

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state. """

        raise NotImplementedError("Overseer update must be implemented")

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. """

        raise NotImplementedError("Overseer iteration_count must be implemented")
