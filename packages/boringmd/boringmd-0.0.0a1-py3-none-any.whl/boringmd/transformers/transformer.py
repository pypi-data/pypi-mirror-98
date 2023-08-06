from abc import ABC, abstractmethod
from typing import Optional

from lstr import lstr

from boringmd.result import Result


class Transformer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def transform(self, index: int, line: lstr) -> Optional[Result]:
        pass
