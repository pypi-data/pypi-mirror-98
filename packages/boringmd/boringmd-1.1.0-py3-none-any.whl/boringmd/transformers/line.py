from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class LineTransformer(Transformer):
    """ Removes lines. """

    def __init__(self) -> None:
        self.previous_was_line = False

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Removes lines.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        if self.previous_was_line and len(line) == 0:
            self.previous_was_line = False
            return LineGuidance(delete=True)

        if line == "---":
            self.previous_was_line = True
            return LineGuidance(delete=True)

        return None
