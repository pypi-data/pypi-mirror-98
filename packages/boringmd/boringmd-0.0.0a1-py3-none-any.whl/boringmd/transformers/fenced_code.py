from typing import Optional

from lstr import lstr

from boringmd.result import Result
from boringmd.transformers.transformer import Transformer


class FencedCodeTransformer(Transformer):
    def __init__(self) -> None:
        self.inside = False

    def transform(self, index: int, line: lstr) -> Optional[Result]:
        if str(line).startswith("```"):
            self.inside = not self.inside
            return Result(delete=True)

        if self.inside:
            return Result(stop=True)

        return None
