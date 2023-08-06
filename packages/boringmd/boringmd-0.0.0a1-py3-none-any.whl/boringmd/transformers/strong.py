from typing import Optional

from lstr import lstr

from boringmd.transformers.transformer import Transformer
from boringmd.result import Result


class StrongTransformer(Transformer):
    def transform(self, index: int, line: lstr) -> Optional[Result]:
        line.sub(r"\*\*([^\*\*]+)\*\*", r"\g<1>")
        return Result(line=line)
