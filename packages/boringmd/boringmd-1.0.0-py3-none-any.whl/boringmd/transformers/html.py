from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class HtmlTransformer(Transformer):
    """ Removes HTML. """

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Removes HTML.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        line.sub(r"(<[^<]*/>)", " ")
        return None
