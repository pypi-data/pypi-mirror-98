from typing import Optional

from lstr import lstr

from boringmd.result import Result
from boringmd.transformers.transformer import Transformer


class IndentedCodeTransformer(Transformer):
    def __init__(self) -> None:
        self.consider_next = False

    def transform(self, index: int, line: lstr) -> Optional[Result]:
        if not self.consider_next:
            self.consider_next = not str(line)

        if not str(line):
            return None

        if str(line).startswith("    "):
            line.lock(0, len(line))
            return Result(line=line)

        self.consider_next = False
        return None
