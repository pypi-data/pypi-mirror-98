from enum import Enum


class MetadataSource(str, Enum):
    SYS = "sys"
    USER = "user"
    EXTRACT = "extract"

    def __str__(self) -> str:
        return str(self.value)
