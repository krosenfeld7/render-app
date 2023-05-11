""" This module provides the different overseers for the world.
    This provides a simple interface for selecting the correct type.
"""

from os import path

from src.classes.exceptions import InvalidHDRIException
from src.classes.overseer import Overseer
from src.classes.world import world
from src.parsers.settings_parser import blender_settings


class WorldOverseer(Overseer):
    """ This class provides the generic world overseer class. This is
        intended to be inherited. """

    def __init__(self,
                 repeat: int) -> None:
        super(WorldOverseer, self).__init__(repeat)
        self._world = world()

    def update(self) -> None:
        raise NotImplementedError("WorldOverseer update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("WorldOverseer iteration_count must be implemented")


class DefaultEmissionOverseer(WorldOverseer):
    """ This class provides the default emission overseer. This simply applies the
        default emission to the world. """

    def __init__(self,
                 repeat: int) -> None:
        super(DefaultEmissionOverseer, self).__init__(repeat)

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state. This overseer simply
            sets the world's emission to the default. """

        world().set_background_emission(blender_settings().background_settings().default_emission())

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. The iteration count will
            always be 1 since this overseer only ever performs one update. """

        return 1

    def __str__(self):
        return 'em' + str(blender_settings().background_settings().default_emission())


class VariableEmissionOverseer(WorldOverseer):
    """ This class provides the variable emission overseer. This applies the specific
        exposure value to the world and changes on each iteration. """

    def __init__(self,
                 repeat: int) -> None:
        super(VariableEmissionOverseer, self).__init__(repeat)
        self._current_emission = 0.0

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state. This overseer sets
            the world's emission based on the emission variability conditions. """

        # only perform updates when required
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        background_settings = blender_settings().background_settings()
        self._current_emission += background_settings.emission_step()
        # update the emission based on the emission step
        if self._current_emission > background_settings.max_emission():
            self._current_emission = background_settings.emission_step()

        self._current_count = 0
        # use the world object to set the emission
        world().set_background_emission(self._current_emission)

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. This is equivalent
            to the number of iterations it takes to utilize each emission value. """

        background_settings = blender_settings().background_settings()
        return max(int(background_settings.max_emission()
                       / background_settings.emission_step()), 1)

    def __str__(self):
        return 'em' + str(self._current_emission)


class HDRIOverseer(WorldOverseer):
    """ This class provides the hdri overseer. This applies the specific
        hdri to the world and changes on each iteration as specified in
        blender_settings.json. """

    def __init__(self,
                 repeat: int) -> None:
        super(HDRIOverseer, self).__init__(repeat)
        self._hdris = blender_settings().background_settings().hdris()
        self._hdri_index = 0

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state. This overseer sets
            the world's hdri in order. """

        # ensure that we are using a valid hdri
        if self._hdri_index >= len(self._hdris):
            raise InvalidHDRIException("Hit an hdri index that is out of the valid range: "
                                       + str(self._hdri_index) + ", max: "
                                       + str(len(self._hdris))
                                       + ", for hdris")

        # only perform the update when required
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        # use the world object to set the hdri
        world().set_hdri(self._hdris[self._hdri_index])
        self._hdri_index += 1
        self._hdri_index %= len(self._hdris)

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. This is equivalent
            to the number of hdris. """

        return len(self._hdris)

    def __str__(self):
        # the current hdri is always one before the index tracker
        current_hdri_index = self._hdri_index - 1
        current_hdri_index %= len(self._hdris)
        return str(path.split(self._hdris[current_hdri_index])[-1])


def world_dispatcher(*args, **kwargs) -> WorldOverseer:
    """ Provides dispatch access to each of the WorldOverseer types based
        upon the settings. """

    if blender_settings().background_settings().hdri_enabled():
        return HDRIOverseer(*args, **kwargs)
    if blender_settings().background_settings().emission_variability_enabled():
        return VariableEmissionOverseer(*args, **kwargs)

    return DefaultEmissionOverseer(*args, **kwargs)
