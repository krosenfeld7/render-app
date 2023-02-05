
class Overseer:
    def __init__(self,
                 repeat: int) -> None:
        self._repeat = max(repeat - 1, 0)
        self._current_count = self._repeat

    def update(self) -> None:
        raise NotImplementedError("Overseer update must be implemented")

    def iteration_count(self) -> int:
        raise NotImplementedError("Overseer iteration_count must be implemented")
