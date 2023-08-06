from typing import Optional

from lstr import lstr


class Result:
    def __init__(
        self,
        delete: bool = False,
        empty: bool = False,
        stop: bool = False,
        line: Optional[lstr] = None,
    ) -> None:
        self.delete = delete
        self.empty = empty
        self.stop = stop
        self.line = line
