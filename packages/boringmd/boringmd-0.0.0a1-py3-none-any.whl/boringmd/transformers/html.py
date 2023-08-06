from typing import Optional

from lstr import lstr

from boringmd.transformers.transformer import Transformer
from boringmd.result import Result


class HtmlTransformer(Transformer):
    def transform(self, index: int, line: lstr) -> Optional[Result]:
        line.sub(r"(<[^<]*/>)", " ")
        return Result(line=line)
