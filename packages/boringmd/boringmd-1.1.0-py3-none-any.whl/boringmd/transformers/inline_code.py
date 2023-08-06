from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class InlineCodeTransformer(Transformer):
    """ Removes fences from inline code. """

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Removes fences from inline code.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        line.sub(r"`([^`]+)`", r"\g<1>", lock=True)
        return None
