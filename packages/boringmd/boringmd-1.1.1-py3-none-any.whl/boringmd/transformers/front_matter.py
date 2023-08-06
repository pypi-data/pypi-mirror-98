from logging import getLogger
from typing import Optional

from lstr import lstr

from boringmd.front_matter import line_delimiter
from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class FrontMatterTransformer(Transformer):
    """ Removes front matter. """

    def __init__(self) -> None:
        self.inside: Optional[str] = None
        self.logger = getLogger("boringmd")

    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Removes front matter.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """

        if line_number > 0 and not self.inside:
            return None

        if line_number == 0:
            d = line_delimiter(str(line))
            if not d:
                # Didn't find a delimiter on this first line, so don't change it.
                return None

            self.inside = d.plain
            self.logger.debug(
                'Deleting "%s" because it starts front matter with delimiter "%s"',
                line,
                self.inside,
            )
            return LineGuidance(delete=True)

        if self.inside and line == self.inside:
            self.inside = None

        self.logger.debug('Deleting "%s" because it\'s front matter.', line)
        return LineGuidance(delete=True)
