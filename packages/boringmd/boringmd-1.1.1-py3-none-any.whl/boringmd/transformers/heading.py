from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class HeadingTransformer(Transformer):
    """ Removes heading markup. """

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Removes heading markup.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        line.sub(r"^(#{1,6}[^#])", "")
        return None
