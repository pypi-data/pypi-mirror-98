from logging import getLogger
from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class FencedCodeTransformer(Transformer):
    """ Removes fences from fenced code. """

    def __init__(self) -> None:
        self.inside: Optional[int] = None
        self.logger = getLogger("boringmd")

    def count(self, line: str, char: str) -> int:
        """
        Count the number of instances of a character at the start of a string.

        Arguments:
            line: String to look at.
            char: Character to look for.

        Returns:
            Number of instances of the character at the start of a string.
        """

        if len(line) == 0:
            return 0

        index = 0
        while index < len(line) and line[index] == char:
            index += 1

        self.logger.debug('Found %s "%s" in "%s"', index, char, line)
        return index

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Removes fences from fenced code.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        count = self.count(str(line), "`")

        if count < 3:
            if self.inside:
                return LineGuidance(stop=True)
            return None

        if self.inside:
            if count == self.inside:
                # We reached the end of the block.
                self.inside = None
                return LineGuidance(delete=True)

            # We're still inside the block. Don't change the line.
            return LineGuidance(stop=True)

        # This starts a fenced block. Count the number of backticks --
        # this block won't be done until we find the same number later.
        self.inside = self.count(str(line), "`")
        return LineGuidance(delete=True)
