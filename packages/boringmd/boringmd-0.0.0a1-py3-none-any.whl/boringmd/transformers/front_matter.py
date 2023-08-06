from typing import Optional

from lstr import lstr

from boringmd.result import Result
from boringmd.transformers.transformer import Transformer


class FrontMatterTransformer(Transformer):
    def __init__(self) -> None:
        self.inside = False

    def transform(self, index: int, line: lstr) -> Optional[Result]:
        if index > 0 and not self.inside:
            return None

        if index == 0:
            if line == "---":
                self.inside = True
                return Result(delete=True)
            return None

        if line == "---":
            self.inside = False

        return Result(delete=True)
