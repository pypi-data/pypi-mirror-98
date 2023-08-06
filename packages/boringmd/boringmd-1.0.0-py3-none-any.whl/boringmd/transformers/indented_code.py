from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class IndentedCodeTransformer(Transformer):
    """ Locks indented code from transformation. """

    def __init__(self) -> None:
        self.consider_next = False

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Locks indented code from transformation.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        if not self.consider_next:
            self.consider_next = not str(line)

        if not str(line):
            return None

        if str(line).startswith("    "):
            line.lock(0, len(line))
            return None

        self.consider_next = False
        return None
