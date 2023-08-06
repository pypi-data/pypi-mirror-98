from abc import ABC, abstractmethod
from typing import Optional

from lstr import lstr

from boringmd.line_guidance import LineGuidance


class Transformer(ABC):
    """ Base implementation for a line transformer. """

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        """ Gets the name of this transformer. """
        return self.__class__.__name__

    @abstractmethod
    def transform(self, line_number: int, line: lstr) -> Optional[LineGuidance]:
        """
        Transforms a line of Markdown into plain text in some way.

        Arguments:
            line_number: Line number of the source document.
            Line:        Line to transform.

        Returns:
            Guidance (if any) for further transformation.
        """
