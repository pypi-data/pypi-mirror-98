from typing import Optional

from lstr import lstr

from boringmd.result import Result
from boringmd.transformers.transformer import Transformer


class HeadingTransformer(Transformer):
    def transform(self, index: int, line: lstr) -> Optional[Result]:
        line.sub(r"^(#{1,6}[^#])", "")
        return Result(line=line)
