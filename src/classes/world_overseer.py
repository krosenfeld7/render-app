from os import path

from src.classes.exceptions import InvalidHDRIException
from src.classes.overseer import Overseer
from src.classes.world import world
from src.parsers.settings_parser import blender_settings


class WorldOverseer(Overseer):

    def __init__(self,
                 repeat: int) -> None:
        super(WorldOverseer, self).__init__(repeat)
        self._world = world()

    def update(self) -> None:
        raise NotImplementedError("WorldOverseer update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("WorldOverseer iteration_count must be implemented")


class DefaultEmissionOverseer(WorldOverseer):

    def __init__(self,
                 repeat: int) -> None:
        super(DefaultEmissionOverseer, self).__init__(repeat)

    def update(self) -> None:
        # update only ensures emission is the default
        world().set_background_emission(blender_settings().background_settings().default_emission())

    def iteration_count(self) -> int:
        return 1

    def __str__(self):
        return 'em' + str(blender_settings().background_settings().default_emission())


class VariableEmissionOverseer(WorldOverseer):

    def __init__(self,
                 repeat: int) -> None:
        super(VariableEmissionOverseer, self).__init__(repeat)
        self._current_emission = 0.0

    def update(self) -> None:
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        background_settings = blender_settings().background_settings()
        self._current_emission += background_settings.emission_step()
        if self._current_emission > background_settings.max_emission():
            self._current_emission = background_settings.emission_step()

        self._current_count = 0
        world().set_background_emission(self._current_emission)

    def iteration_count(self) -> int:
        background_settings = blender_settings().background_settings()
        return max(int(background_settings.max_emission()
                       / background_settings.emission_step()), 1)

    def __str__(self):
        return 'em' + str(self._current_emission)


class HDRIOverseer(WorldOverseer):

    def __init__(self,
                 repeat: int) -> None:
        super(HDRIOverseer, self).__init__(repeat)
        self._hdris = blender_settings().background_settings().hdris()
        self._hdri_index = 0

    def update(self) -> None:
        if self._hdri_index >= len(self._hdris):
            raise InvalidHDRIException("Hit an hdri index that is out of the valid range: "
                                       + str(self._hdri_index) + ", max: "
                                       + str(len(self._hdris))
                                       + ", for hdris")

        if self._current_count < self._repeat:
            self._current_count += 1
            return

        self._current_count = 0
        world().set_hdri(self._hdris[self._hdri_index])
        self._hdri_index += 1
        self._hdri_index %= len(self._hdris)

    def iteration_count(self) -> int:
        return len(self._hdris)

    def __str__(self):
        # the current hdri is one before the index tracker
        current_hdri_index = self._hdri_index - 1
        current_hdri_index %= len(self._hdris)
        return str(path.split(self._hdris[current_hdri_index])[-1])


def world_dispatcher(*args, **kwargs) -> WorldOverseer:
    if blender_settings().background_settings().hdri_enabled():
        return HDRIOverseer(*args, **kwargs)
    if blender_settings().background_settings().emission_variability_enabled():
        return VariableEmissionOverseer(*args, **kwargs)

    return DefaultEmissionOverseer(*args, **kwargs)
