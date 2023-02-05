from bpy import context

from src.classes.overseer import Overseer
from src.parsers.settings_parser import blender_settings


class ViewOverseer(Overseer):

    def __init__(self,
                 repeat: int) -> None:
        super(ViewOverseer, self).__init__(repeat)

    def update(self) -> None:
        raise NotImplementedError("ViewOverseer update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("ViewOverseer iteration_count must be implemented")


class DefaultExposureOverseer(ViewOverseer):

    def __init__(self,
                 repeat: int) -> None:
        super(DefaultExposureOverseer, self).__init__(repeat)

    def update(self) -> None:
        # update only ensures exposure is the default
        context.scene.view_settings.exposure = \
            blender_settings().view_settings().default_exposure()

    def iteration_count(self) -> int:
        return 1

    def __str__(self):
        return 'exp' + str(blender_settings().view_settings().default_exposure())


class VariableExposureOverseer(ViewOverseer):

    def __init__(self,
                 repeat: int) -> None:
        super(VariableExposureOverseer, self).__init__(repeat)
        self._current_exposure = \
            -blender_settings().view_settings().start_exposure() - \
            blender_settings().view_settings().exposure_step()

    def update(self) -> None:
        if self._current_count < self._repeat:
            self._current_count += 1
            return

        view_settings = blender_settings().view_settings()
        self._current_exposure += view_settings.exposure_step()

        if self._current_exposure > view_settings.end_exposure():
            self._current_exposure = view_settings.start_exposure()

        self._current_count = 0
        context.scene.view_settings.exposure = self._current_exposure

    def iteration_count(self) -> int:
        view_settings = blender_settings().view_settings()
        return max(int((view_settings.end_exposure()
                   - view_settings.start_exposure()) / view_settings.exposure_step()) + 1, 1)

    def __str__(self):
        return 'exp' + str(self._current_exposure)


def view_dispatcher(*args, **kwargs) -> ViewOverseer:
    if blender_settings().view_settings().exposure_variability_enabled():
        return VariableExposureOverseer(*args, **kwargs)

    return DefaultExposureOverseer(*args, **kwargs)
