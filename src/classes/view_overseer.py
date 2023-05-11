""" This module provide the different overseers for the view.
    This provides a simple interface for selecting the correct type.
"""

from bpy import context

from src.classes.overseer import Overseer
from src.parsers.settings_parser import blender_settings


class ViewOverseer(Overseer):
    """ This class provides the generic view overseer class. This is
        intended to be inherited. """

    def __init__(self,
                 repeat: int) -> None:
        super(ViewOverseer, self).__init__(repeat)

    def update(self) -> None:
        raise NotImplementedError("ViewOverseer update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("ViewOverseer iteration_count must be implemented")


class DefaultExposureOverseer(ViewOverseer):
    """ This class provides the default exposure overseer. This simply applies the
        default exposure to the scene. """

    def __init__(self,
                 repeat: int) -> None:
        super(DefaultExposureOverseer, self).__init__(repeat)

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state. This overseer simply
            sets the world's exposure to the default. """

        context.scene.view_settings.exposure = \
            blender_settings().view_settings().default_exposure()

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. The iteration count will
            always be 1 since this overseer only ever performs one update. """

        return 1

    def __str__(self):
        return 'exp' + str(blender_settings().view_settings().default_exposure())


class VariableExposureOverseer(ViewOverseer):
    """ This class provides the variable exposure overseer. This applies the specific
        exposure value to the scene and changes on each iteration. """

    def __init__(self,
                 repeat: int) -> None:
        super(VariableExposureOverseer, self).__init__(repeat)
        self._current_exposure = \
            blender_settings().view_settings().start_exposure() - \
            blender_settings().view_settings().exposure_step()

    def update(self) -> None:
        """ Updates this overseer and moves it forward to the next state. This overseer sets
            the world's emission based on the emission variability conditions. """

        # only perform updates when required
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        view_settings = blender_settings().view_settings()
        self._current_exposure += view_settings.exposure_step()
        # update the exposure based on the exposure step
        if self._current_exposure > view_settings.end_exposure():
            self._current_exposure = view_settings.start_exposure()

        self._current_count = 0
        context.scene.view_settings.exposure = self._current_exposure

    def iteration_count(self) -> int:
        """ Returns the iteration count for this overseer. This is equivalent
            to the number of iterations it takes to utilize each exposure value. """

        view_settings = blender_settings().view_settings()
        return max(int((view_settings.end_exposure()
                   - view_settings.start_exposure()) / view_settings.exposure_step()) + 1, 1)

    def __str__(self):
        return 'exp' + str(self._current_exposure)


def view_dispatcher(*args, **kwargs) -> ViewOverseer:
    """ Provides dispatch access to each of the ViewOverseer types based
        upon the settings. """

    if blender_settings().view_settings().exposure_variability_enabled():
        return VariableExposureOverseer(*args, **kwargs)

    return DefaultExposureOverseer(*args, **kwargs)
