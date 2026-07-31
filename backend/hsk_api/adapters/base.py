from typing import Protocol


class LessonGenerator(Protocol):
    def generate(self, *, level: int, size: int) -> object: ...
