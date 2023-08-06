from logging import getLogger
from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance
from boringmd.transformers.transformer import Transformer


class FrontMatterTransformer(Transformer):
    """ Removes front matter. """

    def __init__(self) -> None:
        self.inside = False
        self.logger = getLogger()

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
            if line == "---":
                self.inside = True
                self.logger.debug('Deleting "%s" because it starts front matter.', line)
                return LineGuidance(delete=True)
            return None

        if line == "---":
            self.inside = False

        self.logger.debug('Deleting "%s" because it\'s front matter.', line)
        return LineGuidance(delete=True)
