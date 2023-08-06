from enum import Enum


class ArchiveType(str, Enum):
    ZIP = "zip"

    def __str__(self) -> str:
        return str(self.value)
